using System.Collections.Generic;
using Readarr.Api.V1.Books;
using Readarr.Http;
using RestSharp;

namespace NzbDrone.Integration.Test.Client
{
    public class WantedClient : ClientBase<BookResource>
    {
        public WantedClient(IRestClient restClient, string apiKey, string resource)
            : base(restClient, apiKey, resource)
        {
        }

        public PagingResource<BookResource> GetPagedIncludeAuthor(int pageNumber, int pageSize, string sortKey, string sortDir, string filterKey = null, string filterValue = null, bool includeAuthor = true)
        {
            var request = BuildRequest();
            request.AddQueryParameter("page", pageNumber);
            request.AddQueryParameter("pageSize", pageSize);
            request.AddQueryParameter("sortKey", sortKey);
            request.AddQueryParameter("sortDir", sortDir);

            if (filterKey != null && filterValue != null)
            {
                request.AddQueryParameter("filterKey", filterKey);
                request.AddQueryParameter("filterValue", filterValue);
            }

            request.AddQueryParameter("includeAuthor", includeAuthor);

            return Get<PagingResource<BookResource>>(request);
        }

        public List<BookResource> GetBooksInAuthor(int authorId)
        {
            var request = BuildRequest("?authorId=" + authorId.ToString());
            return Get<List<BookResource>>(request);
        }
    }
}
