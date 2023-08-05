Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("./types");
var utils_1 = require("./utils");
var getListItemDescription = function (rule) {
    var method = rule.method, type = rule.type, source = rule.source;
    var methodLabel = utils_1.getMethodLabel(method);
    var typeLabel = utils_1.getRuleLabel(type);
    var descriptionDetails = [];
    descriptionDetails.push("[" + methodLabel.label + "]");
    descriptionDetails.push(rule.type === types_1.RuleType.PATTERN ? "[" + rule.pattern + "]" : "[" + typeLabel + "]");
    if (rule.method === types_1.MethodType.REPLACE && rule.placeholder) {
        descriptionDetails.push(" with [" + rule.placeholder + "]");
    }
    return descriptionDetails.join(' ') + " " + locale_1.t('from') + " [" + source + "]";
};
var Rules = React.forwardRef(function RulesList(_a, ref) {
    var rules = _a.rules, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled;
    return (<List ref={ref} isDisabled={disabled} data-test-id="advanced-data-scrubbing-rules">
      {rules.map(function (rule) {
            var id = rule.id;
            return (<ListItem key={id}>
            <textOverflow_1.default>{getListItemDescription(rule)}</textOverflow_1.default>
            {onEditRule && (<button_1.default label={locale_1.t('Edit Rule')} size="small" onClick={onEditRule(id)} icon={<icons_1.IconEdit />} disabled={disabled}/>)}
            {onDeleteRule && (<button_1.default label={locale_1.t('Delete Rule')} size="small" onClick={onDeleteRule(id)} icon={<icons_1.IconDelete />} disabled={disabled}/>)}
          </ListItem>);
        })}
    </List>);
});
exports.default = Rules;
var List = styled_1.default('ul')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n  margin-bottom: 0 !important;\n  ", "\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n  margin-bottom: 0 !important;\n  ", "\n"])), function (p) {
    return p.isDisabled &&
        "\n      color: " + p.theme.gray200 + ";\n      background: " + p.theme.backgroundSecondary + ";\n  ";
});
var ListItem = styled_1.default('li')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  &:hover {\n    background-color: ", ";\n  }\n  &:last-child {\n    border-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  &:hover {\n    background-color: ", ";\n  }\n  &:last-child {\n    border-bottom: 0;\n  }\n"])), space_1.default(1), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=rules.jsx.map