Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var rules_1 = tslib_1.__importDefault(require("./rules"));
var utils_1 = require("./utils");
function RulesPanel(_a) {
    var rules = _a.rules, onAddRule = _a.onAddRule, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled, onUpdateRules = _a.onUpdateRules, isErrorPanel = _a.isErrorPanel;
    var panelType = isErrorPanel ? locale_1.t('error') : locale_1.t('transaction');
    return (<panels_1.Panel>
      <rules_1.default rules={rules} onEditRule={onEditRule} onDeleteRule={onDeleteRule} disabled={disabled} onUpdateRules={onUpdateRules} emptyMessage={locale_1.t('There are no %s rules to display', panelType)}/>
      <StyledPanelFooter>
        <buttonBar_1.default gap={1}>
          <button_1.default href={utils_1.DYNAMIC_SAMPLING_DOC_LINK} external>
            {locale_1.t('Read the docs')}
          </button_1.default>
          <button_1.default priority="primary" onClick={onAddRule} disabled={disabled} title={disabled
            ? locale_1.t('You do not have permission to add dynamic sampling rules.')
            : undefined}>
            {locale_1.t('Add %s rule', panelType)}
          </button_1.default>
        </buttonBar_1.default>
      </StyledPanelFooter>
    </panels_1.Panel>);
}
exports.default = RulesPanel;
var StyledPanelFooter = styled_1.default(panels_1.PanelFooter)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  padding: ", " ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])), space_1.default(1), space_1.default(2));
var templateObject_1;
//# sourceMappingURL=rulesPanel.jsx.map