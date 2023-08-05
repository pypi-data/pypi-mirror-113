Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var menu_1 = require("app/components/dropdownAutoComplete/menu");
var index_1 = require("app/components/organizations/timeRangeSelector/index");
function getMediaQueryForSpacer(p) {
    return p.isSpacer
        ? react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n        @media (max-width: ", ") {\n          display: none;\n        }\n      "], ["\n        @media (max-width: ", ") {\n          display: none;\n        }\n      "])), p.theme.breakpoints[1]) : '';
}
var HeaderItemPosition = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  min-width: 0;\n  height: 100%;\n\n  ", "\n\n  ", ", ", " {\n    flex: 1;\n    min-width: 0;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n  min-width: 0;\n  height: 100%;\n\n  ", "\n\n  ", ", ", " {\n    flex: 1;\n    min-width: 0;\n  }\n"])), getMediaQueryForSpacer, menu_1.AutoCompleteRoot, index_1.TimeRangeRoot);
exports.default = HeaderItemPosition;
var templateObject_1, templateObject_2;
//# sourceMappingURL=headerItemPosition.jsx.map