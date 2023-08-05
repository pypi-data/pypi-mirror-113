Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var members_1 = require("app/actionCreators/members");
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
var thresholdControl_1 = tslib_1.__importDefault(require("app/views/alerts/incidentRules/triggers/thresholdControl"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var TriggerForm = /** @class */ (function (_super) {
    tslib_1.__extends(TriggerForm, _super);
    function TriggerForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Handler for threshold changes coming from slider or chart.
         * Needs to sync state with the form.
         */
        _this.handleChangeThreshold = function (value) {
            var _a = _this.props, onChange = _a.onChange, trigger = _a.trigger;
            onChange(tslib_1.__assign(tslib_1.__assign({}, trigger), { alertThreshold: value.threshold }), { alertThreshold: value.threshold });
        };
        return _this;
    }
    TriggerForm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, error = _a.error, trigger = _a.trigger, isCritical = _a.isCritical, thresholdType = _a.thresholdType, fieldHelp = _a.fieldHelp, triggerLabel = _a.triggerLabel, placeholder = _a.placeholder, onThresholdTypeChange = _a.onThresholdTypeChange;
        return (<field_1.default label={triggerLabel} help={fieldHelp} required={isCritical} error={error && error.alertThreshold}>
        <thresholdControl_1.default disabled={disabled} disableThresholdType={!isCritical} type={trigger.label} thresholdType={thresholdType} threshold={trigger.alertThreshold} placeholder={placeholder} onChange={this.handleChangeThreshold} onThresholdTypeChange={onThresholdTypeChange}/>
      </field_1.default>);
    };
    return TriggerForm;
}(React.PureComponent));
var TriggerFormContainer = /** @class */ (function (_super) {
    tslib_1.__extends(TriggerFormContainer, _super);
    function TriggerFormContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeTrigger = function (triggerIndex) { return function (trigger, changeObj) {
            var onChange = _this.props.onChange;
            onChange(triggerIndex, trigger, changeObj);
        }; };
        _this.handleChangeResolveTrigger = function (trigger, _) {
            var onResolveThresholdChange = _this.props.onResolveThresholdChange;
            onResolveThresholdChange(trigger.alertThreshold);
        };
        return _this;
    }
    TriggerFormContainer.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization;
        members_1.fetchOrgMembers(api, organization.slug);
    };
    TriggerFormContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, config = _a.config, disabled = _a.disabled, errors = _a.errors, organization = _a.organization, triggers = _a.triggers, thresholdType = _a.thresholdType, aggregate = _a.aggregate, resolveThreshold = _a.resolveThreshold, projects = _a.projects, onThresholdTypeChange = _a.onThresholdTypeChange;
        var resolveTrigger = {
            label: 'resolve',
            alertThreshold: resolveThreshold,
            actions: [],
        };
        var thresholdUnits = aggregate.includes('duration') || aggregate.includes('measurements')
            ? 'ms'
            : aggregate.includes('failure_rate')
                ? '%'
                : '';
        return (<React.Fragment>
        {triggers.map(function (trigger, index) {
                var isCritical = index === 0;
                // eslint-disable-next-line no-use-before-define
                var TriggerIndicator = isCritical ? CriticalIndicator : WarningIndicator;
                return (<TriggerForm key={index} api={api} config={config} disabled={disabled} error={errors && errors.get(index)} trigger={trigger} thresholdType={thresholdType} aggregate={aggregate} resolveThreshold={resolveThreshold} organization={organization} projects={projects} triggerIndex={index} isCritical={isCritical} fieldHelp={locale_1.tct('The threshold[units] that will activate the [severity] status.', {
                        severity: isCritical ? locale_1.t('critical') : locale_1.t('warning'),
                        units: thresholdUnits ? " (" + thresholdUnits + ")" : '',
                    })} triggerLabel={<React.Fragment>
                  <TriggerIndicator size={12}/>
                  {isCritical ? locale_1.t('Critical') : locale_1.t('Warning')}
                </React.Fragment>} placeholder={isCritical ? "300" + thresholdUnits : locale_1.t('None')} onChange={_this.handleChangeTrigger(index)} onThresholdTypeChange={onThresholdTypeChange}/>);
            })}
        <TriggerForm api={api} config={config} disabled={disabled} error={errors && errors.get(2)} trigger={resolveTrigger} 
        // Flip rule thresholdType to opposite
        thresholdType={+!thresholdType} aggregate={aggregate} resolveThreshold={resolveThreshold} organization={organization} projects={projects} triggerIndex={2} isCritical={false} fieldHelp={locale_1.tct('The threshold[units] that will activate the resolved status.', {
                units: thresholdUnits ? " (" + thresholdUnits + ")" : '',
            })} triggerLabel={<React.Fragment>
              <ResolvedIndicator size={12}/>
              {locale_1.t('Resolved')}
            </React.Fragment>} placeholder={locale_1.t('Automatic')} onChange={this.handleChangeResolveTrigger} onThresholdTypeChange={onThresholdTypeChange}/>
      </React.Fragment>);
    };
    return TriggerFormContainer;
}(React.Component));
var CriticalIndicator = styled_1.default(circleIndicator_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  margin-right: ", ";\n"], ["\n  background: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.red300; }, space_1.default(1));
var WarningIndicator = styled_1.default(circleIndicator_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  margin-right: ", ";\n"], ["\n  background: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.yellow300; }, space_1.default(1));
var ResolvedIndicator = styled_1.default(circleIndicator_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  margin-right: ", ";\n"], ["\n  background: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.green300; }, space_1.default(1));
exports.default = withConfig_1.default(withApi_1.default(TriggerFormContainer));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=form.jsx.map