Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var summary_1 = tslib_1.__importDefault(require("./summary"));
var Http = function (_a) {
    var breadcrumb = _a.breadcrumb, searchTerm = _a.searchTerm;
    var data = breadcrumb.data;
    var renderUrl = function (url) {
        if (typeof url === 'string') {
            var content = <highlight_1.default text={searchTerm}>{url}</highlight_1.default>;
            return url.match(/^https?:\/\//) ? (<externalLink_1.default data-test-id="http-renderer-external-link" href={url}>
          {content}
        </externalLink_1.default>) : (<span>{content}</span>);
        }
        try {
            return <highlight_1.default text={searchTerm}>{JSON.stringify(url)}</highlight_1.default>;
        }
        catch (_a) {
            return locale_1.t('Invalid URL');
        }
    };
    var statusCode = data === null || data === void 0 ? void 0 : data.status_code;
    return (<summary_1.default kvData={omit_1.default(data, ['method', 'url', 'status_code'])}>
      {(data === null || data === void 0 ? void 0 : data.method) && (<annotatedText_1.default value={<strong>
              <highlight_1.default text={searchTerm}>{data.method + " "}</highlight_1.default>
            </strong>} meta={metaProxy_1.getMeta(data, 'method')}/>)}
      {(data === null || data === void 0 ? void 0 : data.url) && (<annotatedText_1.default value={renderUrl(data.url)} meta={metaProxy_1.getMeta(data, 'url')}/>)}
      {utils_1.defined(statusCode) && (<annotatedText_1.default value={<highlight_1.default data-test-id="http-renderer-status-code" text={searchTerm}>{" [" + statusCode + "]"}</highlight_1.default>} meta={metaProxy_1.getMeta(data, 'status_code')}/>)}
    </summary_1.default>);
};
exports.default = Http;
//# sourceMappingURL=http.jsx.map