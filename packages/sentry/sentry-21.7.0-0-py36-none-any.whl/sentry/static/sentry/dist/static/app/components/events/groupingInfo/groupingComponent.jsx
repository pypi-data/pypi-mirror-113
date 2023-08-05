Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupingValue = exports.GroupingComponentListItem = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var groupingComponentChildren_1 = tslib_1.__importDefault(require("./groupingComponentChildren"));
var groupingComponentStacktrace_1 = tslib_1.__importDefault(require("./groupingComponentStacktrace"));
var utils_1 = require("./utils");
var GroupingComponent = function (_a) {
    var component = _a.component, showNonContributing = _a.showNonContributing;
    var shouldInlineValue = utils_1.shouldInlineComponentValue(component);
    var GroupingComponentListItems = component.id === 'stacktrace'
        ? groupingComponentStacktrace_1.default
        : groupingComponentChildren_1.default;
    return (<GroupingComponentWrapper isContributing={component.contributes}>
      <span>
        {component.name || component.id}
        {component.hint && <GroupingHint>{" (" + component.hint + ")"}</GroupingHint>}
      </span>

      <GroupingComponentList isInline={shouldInlineValue}>
        <GroupingComponentListItems component={component} showNonContributing={showNonContributing}/>
      </GroupingComponentList>
    </GroupingComponentWrapper>);
};
var GroupingComponentList = styled_1.default('ul')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  margin: 0;\n  list-style: none;\n  &,\n  & > li {\n    display: ", ";\n  }\n"], ["\n  padding: 0;\n  margin: 0;\n  list-style: none;\n  &,\n  & > li {\n    display: ", ";\n  }\n"])), function (p) { return (p.isInline ? 'inline' : 'block'); });
exports.GroupingComponentListItem = styled_1.default('li')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  margin: ", " 0 ", " ", ";\n\n  ", "\n"], ["\n  padding: 0;\n  margin: ", " 0 ", " ", ";\n\n  ", "\n"])), space_1.default(0.25), space_1.default(0.25), space_1.default(1.5), function (p) {
    return p.isCollapsable &&
        "\n    border-left: 1px solid " + p.theme.innerBorder + ";\n    margin: 0 0 -" + space_1.default(0.25) + " " + space_1.default(1) + ";\n    padding-left: " + space_1.default(0.5) + ";\n  ";
});
exports.GroupingValue = styled_1.default('code')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin: ", " ", " ", " 0;\n  font-size: ", ";\n  padding: 0 ", ";\n  background: rgba(112, 163, 214, 0.1);\n  color: ", ";\n\n  ", "\n"], ["\n  display: inline-block;\n  margin: ", " ", " ", " 0;\n  font-size: ", ";\n  padding: 0 ", ";\n  background: rgba(112, 163, 214, 0.1);\n  color: ", ";\n\n  ", "\n"])), space_1.default(0.25), space_1.default(0.5), space_1.default(0.25), function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.25), function (p) { return p.theme.textColor; }, function (_a) {
    var valueType = _a.valueType;
    return (valueType === 'function' || valueType === 'symbol') &&
        "\n    font-weight: bold;\n    color: " + function (p) { return p.theme.textColor; } + ";\n  ";
});
var GroupingComponentWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n\n  ", ", button {\n    opacity: 1;\n  }\n"], ["\n  color: ", ";\n\n  ", ", button {\n    opacity: 1;\n  }\n"])), function (p) { return (p.isContributing ? null : p.theme.textColor); }, exports.GroupingValue);
var GroupingHint = styled_1.default('small')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: 0.8em;\n"], ["\n  font-size: 0.8em;\n"])));
exports.default = GroupingComponent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=groupingComponent.jsx.map