using System;
using Moq;
using NLog;
using NUnit.Framework;
using NzbDrone.Common.Disk;
using Readarr.Http.Frontend.Mappers;

namespace NzbDrone.Api.Test.Frontend
{
    [TestFixture]
    public class HtmlMapperBaseFixture
    {
        [TestCase("\"/index.js\"")]
        [TestCase("'/index.js'")]
        [TestCase("/index.js")]
        public void applies_url_base_to_minified_asset_attributes(string scriptUrl)
        {
            var disk = new Mock<IDiskProvider>();
            disk.Setup(provider => provider.ReadAllText("index.html"))
                .Returns($"<script src={scriptUrl} data-no-hash></script><link href=/Content/styles.css>");
            var cacheBreaker = new Mock<ICacheBreakerProvider>(MockBehavior.Strict);
            cacheBreaker.Setup(provider => provider.AddCacheBreakerToPath("/Content/styles.css"))
                .Returns("/Content/styles.css?h=test");

            var html = new TestHtmlMapper(disk.Object, cacheBreaker.Object).Render();

            Assert.That(html, Is.EqualTo("<script src=\"/bookshelf/index.js\"></script><link href=\"/bookshelf/Content/styles.css?h=test\">"));
        }

        private sealed class TestHtmlMapper : HtmlMapperBase
        {
            public TestHtmlMapper(IDiskProvider disk, ICacheBreakerProvider cacheBreaker)
                : base(disk, new Lazy<ICacheBreakerProvider>(() => cacheBreaker), LogManager.GetCurrentClassLogger())
            {
                HtmlPath = "index.html";
                UrlBase = "/bookshelf";
            }

            public string Render() => GetHtmlText();

            public override string Map(string resourceUrl) => HtmlPath;

            public override bool CanHandle(string resourceUrl) => true;
        }
    }
}
