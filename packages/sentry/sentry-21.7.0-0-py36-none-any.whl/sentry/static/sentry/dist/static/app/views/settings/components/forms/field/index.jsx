/**
 * A component to render a Field (i.e. label + help + form "control"),
 * generally inside of a Panel.
 *
 * This is unconnected to any Form state
 */
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var controlState_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/controlState"));
var fieldControl_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldControl"));
var fieldDescription_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldDescription"));
var fieldErrorReason_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldErrorReason"));
var fieldHelp_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldHelp"));
var fieldLabel_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldLabel"));
var fieldRequiredBadge_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldRequiredBadge"));
var fieldWrapper_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldWrapper"));
var fieldQuestion_1 = tslib_1.__importDefault(require("./fieldQuestion"));
var Field = /** @class */ (function (_super) {
    tslib_1.__extends(Field, _super);
    function Field() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Field.prototype.render = function () {
        var _a = this.props, className = _a.className, otherProps = tslib_1.__rest(_a, ["className"]);
        var controlClassName = otherProps.controlClassName, alignRight = otherProps.alignRight, inline = otherProps.inline, highlighted = otherProps.highlighted, required = otherProps.required, visible = otherProps.visible, disabled = otherProps.disabled, disabledReason = otherProps.disabledReason, error = otherProps.error, flexibleControlStateSize = otherProps.flexibleControlStateSize, help = otherProps.help, id = otherProps.id, isSaving = otherProps.isSaving, isSaved = otherProps.isSaved, label = otherProps.label, hideLabel = otherProps.hideLabel, stacked = otherProps.stacked, children = otherProps.children, style = otherProps.style, showHelpInTooltip = otherProps.showHelpInTooltip;
        var isDisabled = typeof disabled === 'function' ? disabled(this.props) : disabled;
        var isVisible = typeof visible === 'function' ? visible(this.props) : visible;
        var Control;
        if (!isVisible) {
            return null;
        }
        var helpElement = typeof help === 'function' ? help(this.props) : help;
        var controlProps = {
            className: controlClassName,
            inline: inline,
            alignRight: alignRight,
            disabled: isDisabled,
            disabledReason: disabledReason,
            flexibleControlStateSize: flexibleControlStateSize,
            help: helpElement,
            errorState: error ? <fieldErrorReason_1.default>{error}</fieldErrorReason_1.default> : null,
            controlState: <controlState_1.default error={error} isSaving={isSaving} isSaved={isSaved}/>,
        };
        // See comments in prop types
        if (children instanceof Function) {
            Control = children(tslib_1.__assign(tslib_1.__assign({}, otherProps), controlProps));
        }
        else {
            Control = <fieldControl_1.default {...controlProps}>{children}</fieldControl_1.default>;
        }
        return (<fieldWrapper_1.default className={className} inline={inline} stacked={stacked} highlighted={highlighted} hasControlState={!flexibleControlStateSize} style={style}>
        {((label && !hideLabel) || helpElement) && (<fieldDescription_1.default inline={inline} htmlFor={id}>
            {label && !hideLabel && (<fieldLabel_1.default disabled={isDisabled}>
                <span>
                  {label}
                  {required && <fieldRequiredBadge_1.default />}
                </span>
                {helpElement && showHelpInTooltip && (<fieldQuestion_1.default>
                    <questionTooltip_1.default position="top" size="sm" title={helpElement}/>
                  </fieldQuestion_1.default>)}
              </fieldLabel_1.default>)}
            {helpElement && !showHelpInTooltip && (<fieldHelp_1.default stacked={stacked} inline={inline}>
                {helpElement}
              </fieldHelp_1.default>)}
          </fieldDescription_1.default>)}

        {Control}
      </fieldWrapper_1.default>);
    };
    Field.defaultProps = {
        alignRight: false,
        inline: true,
        disabled: false,
        required: false,
        visible: true,
        showHelpInTooltip: false,
    };
    return Field;
}(React.Component));
exports.default = Field;
//# sourceMappingURL=index.jsx.map