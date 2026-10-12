using System;
using System.IO;
using NzbDrone.Common.Disk;
using NzbDrone.Common.EnvironmentInfo;
using SkiaSharp;

namespace NzbDrone.Core.MediaCover
{
    public interface IImageResizer
    {
        void Resize(string source, string destination, int height);
    }

    public class ImageResizer : IImageResizer
    {
        private static readonly SKSamplingOptions ResizeSampling = new SKSamplingOptions(SKFilterMode.Linear, SKMipmapMode.Linear);

        private readonly IDiskProvider _diskProvider;
        private readonly bool _enabled;

        public ImageResizer(IDiskProvider diskProvider, IPlatformInfo platformInfo)
        {
            _diskProvider = diskProvider;

            // SkiaSharp does not ship FreeBSD native assets. The cover endpoint
            // falls back to the original file when a resized image is missing.
            _enabled = !OperatingSystem.IsFreeBSD();
        }

        public void Resize(string source, string destination, int height)
        {
            if (!_enabled)
            {
                return;
            }

            try
            {
                var extension = Path.GetExtension(destination).ToLowerInvariant();
                var format = extension switch
                {
                    ".jpg" or ".jpeg" => SKEncodedImageFormat.Jpeg,
                    ".png" => SKEncodedImageFormat.Png,
                    _ => (SKEncodedImageFormat?)null
                };

                if (!format.HasValue)
                {
                    File.Copy(source, destination, true);
                    return;
                }

                using var image = SKBitmap.Decode(source);
                if (image == null)
                {
                    throw new InvalidDataException($"Could not decode image: {source}");
                }

                var targetWidth = Math.Max(1, (int)Math.Round((double)image.Width * height / image.Height));
                using var surface = SKSurface.Create(new SKImageInfo(targetWidth, height));
                surface.Canvas.DrawBitmap(image, new SKRect(0, 0, targetWidth, height), ResizeSampling);

                using var resizedImage = surface.Snapshot();
                using var encodedImage = resizedImage.Encode(format.Value, format == SKEncodedImageFormat.Jpeg ? 92 : 100);
                using var output = File.Create(destination);
                encodedImage.SaveTo(output);
            }
            catch
            {
                if (_diskProvider.FileExists(destination))
                {
                    _diskProvider.DeleteFile(destination);
                }

                throw;
            }
        }
    }
}
