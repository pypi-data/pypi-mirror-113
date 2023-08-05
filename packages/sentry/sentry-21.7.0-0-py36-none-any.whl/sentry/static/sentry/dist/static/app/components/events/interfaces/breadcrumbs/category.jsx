Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var Category = react_1.memo(function (_a) {
    var category = _a.category, searchTerm = _a.searchTerm;
    var title = !utils_1.defined(category) ? locale_1.t('generic') : category;
    return (<Wrapper title={title}>
      <tooltip_1.default title={title} containerDisplayMode="inline-flex">
        <textOverflow_1.default>
          <highlight_1.default text={searchTerm}>{title}</highlight_1.default>
        </textOverflow_1.default>
      </tooltip_1.default>
    </Wrapper>);
});
exports.default = Category;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 700;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 700;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=category.jsx.map