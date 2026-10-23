using System;
using System.Collections.Generic;
using System.Linq;
using FluentAssertions;
using Moq;
using NUnit.Framework;
using NzbDrone.Common.Cloud;
using NzbDrone.Common.EnvironmentInfo;
using NzbDrone.Common.Extensions;
using NzbDrone.Common.Http;
using NzbDrone.Common.Serializer;
using NzbDrone.Core.Test.Framework;
using NzbDrone.Core.Update;

namespace NzbDrone.Core.Test.UpdateTests
{
    public class UpdatePackageProviderFixture : CoreTest<UpdatePackageProvider>
    {
        [SetUp]
        public void Setup()
        {
            Mocker.GetMock<IPlatformInfo>().SetupGet(c => c.Version).Returns(new Version("9.9.9"));
            Mocker.SetConstant<IReadarrCloudRequestBuilder>(new ReadarrCloudRequestBuilder());
        }

        private void GivenResponse<T>(T response)
            where T : new()
        {
            var json = response.ToJson();

            Mocker.GetMock<IHttpClient>()
                .Setup(c => c.Get<T>(It.IsAny<HttpRequest>()))
                .Returns<HttpRequest>(request => new HttpResponse<T>(new HttpResponse(request, new HttpHeader(), json)));
        }

        [Test]
        public void no_update_when_version_higher()
        {
            GivenResponse(new UpdatePackageAvailable { Available = false });

            Subject.GetLatestUpdate("develop", new Version(10, 0)).Should().BeNull();
        }

        [Test]
        public void finds_update_when_version_lower()
        {
            GivenResponse(new UpdatePackageAvailable
            {
                Available = true,
                UpdatePackage = new UpdatePackage { Version = new Version(1, 0) }
            });

            var update = Subject.GetLatestUpdate("develop", new Version(0, 1));

            update.Should().NotBeNull();
            update.Version.Should().Be(new Version(1, 0));
        }

        [Test]
        [Ignore("Ignore until we actually release something on Master")]
        public void should_get_master_if_branch_doesnt_exit()
        {
            UseRealHttp();
            Subject.GetLatestUpdate("invalid_branch", new Version(0, 2)).Should().NotBeNull();
        }

        [Test]
        public void should_get_recent_updates()
        {
            const string branch = "develop";

            GivenResponse(new List<UpdatePackage>
            {
                new UpdatePackage
                {
                    Version = new Version(1, 0),
                    ReleaseDate = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                    FileName = "Readarr.develop.0.1.0.1234.linux-core-x64.tar.gz",
                    Hash = "test-hash",
                    Branch = branch,
                    Changes = new UpdateChanges
                    {
                        New = new List<string> { "New feature" },
                        Fixed = new List<string> { "Bug fix" }
                    }
                }
            });

            var recent = Subject.GetRecentUpdates(branch, new Version(0, 1), null);

            recent.Should().NotBeEmpty();
            recent.Should().OnlyContain(c => c.Hash.IsNotNullOrWhiteSpace());
            recent.Should().OnlyContain(c => c.FileName.Contains("Readarr.develop.0"));
            recent.Should().OnlyContain(c => c.ReleaseDate.Year >= 2014);
            recent.Where(c => c.Changes != null).Should().OnlyContain(c => c.Changes.New != null);
            recent.Where(c => c.Changes != null).Should().OnlyContain(c => c.Changes.Fixed != null);
            recent.Should().OnlyContain(c => c.Branch == branch);
        }
    }
}
