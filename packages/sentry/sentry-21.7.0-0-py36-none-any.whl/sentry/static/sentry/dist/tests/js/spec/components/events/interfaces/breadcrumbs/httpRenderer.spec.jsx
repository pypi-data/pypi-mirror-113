Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var http_1 = tslib_1.__importDefault(require("app/components/events/interfaces/breadcrumbs/data/http"));
var breadcrumbs_1 = require("app/types/breadcrumbs");
describe('HttpRenderer', function () {
    describe('render', function () {
        it('should work', function () {
            var httpRendererWrapper = enzyme_1.mountWithTheme(<http_1.default searchTerm="" breadcrumb={{
                    type: breadcrumbs_1.BreadcrumbType.HTTP,
                    level: breadcrumbs_1.BreadcrumbLevelType.INFO,
                    data: {
                        method: 'POST',
                        url: 'http://example.com/foo',
                        // status_code 0 is possible via broken client-side XHR; should still render as '[0]'
                        status_code: 0,
                    },
                }}/>);
            var annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(3);
            expect(annotatedTexts.at(0).find('strong').text()).toEqual('POST ');
            expect(annotatedTexts.at(1).find('a[data-test-id="http-renderer-external-link"]').text()).toEqual('http://example.com/foo');
            expect(annotatedTexts
                .at(2)
                .find('Highlight[data-test-id="http-renderer-status-code"]')
                .text()).toEqual(' [0]');
        });
        it("shouldn't blow up if crumb.data is missing", function () {
            var httpRendererWrapper = enzyme_1.mountWithTheme(<http_1.default searchTerm="" breadcrumb={{
                    category: 'xhr',
                    type: breadcrumbs_1.BreadcrumbType.HTTP,
                    level: breadcrumbs_1.BreadcrumbLevelType.INFO,
                }}/>);
            var annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(0);
        });
        it("shouldn't blow up if url is not a string", function () {
            var httpRendererWrapper = enzyme_1.mountWithTheme(<http_1.default searchTerm="" breadcrumb={{
                    category: 'xhr',
                    type: breadcrumbs_1.BreadcrumbType.HTTP,
                    level: breadcrumbs_1.BreadcrumbLevelType.INFO,
                    data: {
                        method: 'GET',
                    },
                }}/>);
            var annotatedTexts = httpRendererWrapper.find('AnnotatedText');
            expect(annotatedTexts.length).toEqual(1);
        });
    });
});
//# sourceMappingURL=httpRenderer.spec.jsx.map