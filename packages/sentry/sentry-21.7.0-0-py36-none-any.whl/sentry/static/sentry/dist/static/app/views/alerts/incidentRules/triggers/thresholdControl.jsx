Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var numberDragControl_1 = tslib_1.__importDefault(require("app/components/numberDragControl"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/views/alerts/incidentRules/types");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var ThresholdControl = /** @class */ (function (_super) {
    tslib_1.__extends(ThresholdControl, _super);
    function ThresholdControl() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            currentValue: null,
        };
        _this.handleThresholdChange = function (e) {
            var value = e.target.value;
            // Only allow number and partial number inputs
            if (!/^[0-9]*\.?[0-9]*$/.test(value)) {
                return;
            }
            var _a = _this.props, onChange = _a.onChange, thresholdType = _a.thresholdType;
            // Empty input
            if (value === '') {
                _this.setState({ currentValue: null });
                onChange({ thresholdType: thresholdType, threshold: '' }, e);
                return;
            }
            // Only call onChange if the new number is valid, and not partially typed
            // (eg writing out the decimal '5.')
            if (/\.+0*$/.test(value)) {
                _this.setState({ currentValue: value });
                return;
            }
            var numberValue = Number(value);
            _this.setState({ currentValue: null });
            onChange({ thresholdType: thresholdType, threshold: numberValue }, e);
        };
        /**
         * Coerce the currentValue to a number and trigger the onChange.
         */
        _this.handleThresholdBlur = function (e) {
            if (_this.state.currentValue === null) {
                return;
            }
            var _a = _this.props, onChange = _a.onChange, thresholdType = _a.thresholdType;
            onChange({ thresholdType: thresholdType, threshold: Number(_this.state.currentValue) }, e);
            _this.setState({ currentValue: null });
        };
        _this.handleTypeChange = function (_a, _) {
            var value = _a.value;
            var onThresholdTypeChange = _this.props.onThresholdTypeChange;
            onThresholdTypeChange(value);
        };
        _this.handleDragChange = function (delta, e) {
            var _a = _this.props, onChange = _a.onChange, thresholdType = _a.thresholdType, threshold = _a.threshold;
            var currentValue = threshold || 0;
            onChange({ thresholdType: thresholdType, threshold: currentValue + delta }, e);
        };
        return _this;
    }
    ThresholdControl.prototype.render = function () {
        var _a;
        var currentValue = this.state.currentValue;
        var _b = this.props, thresholdType = _b.thresholdType, threshold = _b.threshold, placeholder = _b.placeholder, type = _b.type, _ = _b.onChange, __ = _b.onThresholdTypeChange, disabled = _b.disabled, disableThresholdType = _b.disableThresholdType, props = tslib_1.__rest(_b, ["thresholdType", "threshold", "placeholder", "type", "onChange", "onThresholdTypeChange", "disabled", "disableThresholdType"]);
        return (<div {...props}>
        <selectControl_1.default isDisabled={disabled || disableThresholdType} name={type + "ThresholdType"} value={thresholdType} options={[
                { value: types_1.AlertRuleThresholdType.BELOW, label: locale_1.t('Below') },
                { value: types_1.AlertRuleThresholdType.ABOVE, label: locale_1.t('Above') },
            ]} components={disableThresholdType ? { DropdownIndicator: null } : null} styles={disableThresholdType
                ? {
                    control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { cursor: 'not-allowed', pointerEvents: 'auto' })); },
                }
                : null} onChange={this.handleTypeChange}/>
        <StyledInput disabled={disabled} name={type + "Threshold"} placeholder={placeholder} value={(_a = currentValue !== null && currentValue !== void 0 ? currentValue : threshold) !== null && _a !== void 0 ? _a : ''} onChange={this.handleThresholdChange} onBlur={this.handleThresholdBlur} 
        // Disable lastpass autocomplete
        data-lpignore="true"/>
        <DragContainer>
          <tooltip_1.default title={locale_1.tct('Drag to adjust threshold[break]You can hold shift to fine tune', {
                break: <br />,
            })}>
            <numberDragControl_1.default step={5} axis="y" onChange={this.handleDragChange}/>
          </tooltip_1.default>
        </DragContainer>
      </div>);
    };
    return ThresholdControl;
}(React.Component));
var StyledInput = styled_1.default(input_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* Match the height of the select controls */\n  height: 40px;\n"], ["\n  /* Match the height of the select controls */\n  height: 40px;\n"])));
var DragContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 4px;\n  right: 12px;\n"], ["\n  position: absolute;\n  top: 4px;\n  right: 12px;\n"])));
exports.default = styled_1.default(ThresholdControl)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: grid;\n  align-items: center;\n  grid-template-columns: 1fr 3fr;\n  grid-gap: ", ";\n"], ["\n  position: relative;\n  display: grid;\n  align-items: center;\n  grid-template-columns: 1fr 3fr;\n  grid-gap: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=thresholdControl.jsx.map