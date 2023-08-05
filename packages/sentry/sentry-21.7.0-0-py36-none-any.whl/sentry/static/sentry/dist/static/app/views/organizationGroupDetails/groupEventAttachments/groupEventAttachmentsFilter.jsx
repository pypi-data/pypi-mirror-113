Object.defineProperty(exports, "__esModule", { value: true });
exports.crashReportTypes = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var xor_1 = tslib_1.__importDefault(require("lodash/xor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var crashReportTypes = ['event.minidump', 'event.applecrashreport'];
exports.crashReportTypes = crashReportTypes;
var GroupEventAttachmentsFilter = function (props) {
    var _a = props.location, query = _a.query, pathname = _a.pathname;
    var types = query.types;
    var allAttachmentsQuery = omit_1.default(query, 'types');
    var onlyCrashReportsQuery = tslib_1.__assign(tslib_1.__assign({}, query), { types: crashReportTypes });
    var activeButton = '';
    if (types === undefined) {
        activeButton = 'all';
    }
    else if (xor_1.default(crashReportTypes, types).length === 0) {
        activeButton = 'onlyCrash';
    }
    return (<FilterWrapper>
      <buttonBar_1.default merged active={activeButton}>
        <button_1.default barId="all" size="small" to={{ pathname: pathname, query: allAttachmentsQuery }}>
          {locale_1.t('All Attachments')}
        </button_1.default>
        <button_1.default barId="onlyCrash" size="small" to={{ pathname: pathname, query: onlyCrashReportsQuery }}>
          {locale_1.t('Only Crash Reports')}
        </button_1.default>
      </buttonBar_1.default>
    </FilterWrapper>);
};
var FilterWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.default = react_router_1.withRouter(GroupEventAttachmentsFilter);
var templateObject_1;
//# sourceMappingURL=groupEventAttachmentsFilter.jsx.map