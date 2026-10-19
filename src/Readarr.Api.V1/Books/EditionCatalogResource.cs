using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using NzbDrone.Core.Books;

namespace Readarr.Api.V1.Books
{
    /// <summary>
    /// One edition in terms a person chooses between, using the same shape as Chaptarr's edition
    /// catalog so SeerrNG reads both. Bookshelf stores a single narrator string, so production and
    /// abridgement are reported only when the edition's own text says so.
    /// </summary>
    public class EditionCatalogResource
    {
        public int EditionId { get; set; }
        public string ForeignEditionId { get; set; }
        public string Title { get; set; }
        public string Language { get; set; }
        public string Format { get; set; }
        public bool IsEbook { get; set; }
        public List<string> Narrators { get; set; } = new List<string>();
        public string Production { get; set; } = "unknown";
        public string Abridged { get; set; } = "unknown";
        public int? DurationSeconds { get; set; }
        public string Publisher { get; set; }
        public DateTime? ReleaseDate { get; set; }
        public string ImageUrl { get; set; }
        public bool Monitored { get; set; }
        public bool Owned { get; set; }
    }

    public static class EditionCatalogMapper
    {
        private static readonly Regex Unabridged = new Regex(@"\bunabridged\b", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        private static readonly Regex Abridged = new Regex(@"\babridged\b", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        private static readonly Regex FullCast = new Regex(@"\b(full[- ]?cast|dramati[sz]ed|graphic ?audio|multi[- ]?cast)\b", RegexOptions.IgnoreCase | RegexOptions.Compiled);

        public static List<string> NarratorsOf(Edition edition)
        {
            return (edition.Narrator ?? string.Empty)
                .Split(new[] { ',', ';', '&' }, StringSplitOptions.RemoveEmptyEntries)
                .Select(n => n.Trim())
                .Where(n => n.Length > 0)
                .Distinct(StringComparer.OrdinalIgnoreCase)
                .ToList();
        }

        public static EditionCatalogResource ToCatalogResource(this Edition edition)
        {
            var narrators = NarratorsOf(edition);
            var hints = string.Join(" ", new[] { edition.Title, edition.Disambiguation });
            var production = "unknown";
            if (!edition.IsEbook)
            {
                production = FullCast.IsMatch(hints) ? "full-cast" : narrators.Count == 1 ? "solo" : "unknown";
            }

            var abridged = "unknown";
            if (!edition.IsEbook)
            {
                abridged = Unabridged.IsMatch(hints) ? "unabridged" : Abridged.IsMatch(hints) ? "abridged" : "unknown";
            }

            var cover = edition.Images?.FirstOrDefault(i => i.CoverType == NzbDrone.Core.MediaCover.MediaCoverTypes.Cover);
            return new EditionCatalogResource
            {
                EditionId = edition.Id,
                ForeignEditionId = edition.ForeignEditionId,
                Title = edition.Title,
                Language = edition.Language,
                Format = edition.Format,
                IsEbook = edition.IsEbook,
                Narrators = narrators,
                Production = production,
                Abridged = abridged,
                Publisher = edition.Publisher,
                ReleaseDate = edition.ReleaseDate,
                ImageUrl = cover?.RemoteUrl ?? cover?.Url,
                Monitored = edition.Monitored,
                Owned = edition.BookFiles?.IsLoaded == true && edition.BookFiles.Value.Any()
            };
        }
    }
}
