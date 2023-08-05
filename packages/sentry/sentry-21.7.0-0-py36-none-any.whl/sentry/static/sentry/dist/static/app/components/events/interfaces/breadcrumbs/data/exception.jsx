Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var utils_1 = require("app/utils");
var summary_1 = tslib_1.__importDefault(require("./summary"));
var Exception = function (_a) {
    var breadcrumb = _a.breadcrumb, searchTerm = _a.searchTerm;
    var data = breadcrumb.data;
    var dataValue = data === null || data === void 0 ? void 0 : data.value;
    return (<summary_1.default kvData={omit_1.default(data, ['type', 'value'])}>
      {(data === null || data === void 0 ? void 0 : data.type) && (<annotatedText_1.default value={<strong>
              <highlight_1.default text={searchTerm}>{data.type + ": "}</highlight_1.default>
            </strong>} meta={metaProxy_1.getMeta(data, 'type')}/>)}
      {utils_1.defined(dataValue) && (<annotatedText_1.default value={<highlight_1.default text={searchTerm}>
              {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) ? dataValue + ". " : dataValue}
            </highlight_1.default>} meta={metaProxy_1.getMeta(data, 'value')}/>)}
      {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) && (<annotatedText_1.default value={<highlight_1.default text={searchTerm}>{breadcrumb.message}</highlight_1.default>} meta={metaProxy_1.getMeta(breadcrumb, 'message')}/>)}
    </summary_1.default>);
};
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map