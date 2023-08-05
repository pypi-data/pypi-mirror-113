Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var panels_1 = require("app/components/panels");
var sanitizeQuerySelector_1 = require("app/utils/sanitizeQuerySelector");
var fieldFromConfig_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/fieldFromConfig"));
var FormPanel = /** @class */ (function (_super) {
    tslib_1.__extends(FormPanel, _super);
    function FormPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FormPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, title = _a.title, fields = _a.fields, access = _a.access, disabled = _a.disabled, additionalFieldProps = _a.additionalFieldProps, renderFooter = _a.renderFooter, renderHeader = _a.renderHeader, otherProps = tslib_1.__rest(_a, ["title", "fields", "access", "disabled", "additionalFieldProps", "renderFooter", "renderHeader"]);
        return (<panels_1.Panel id={typeof title === 'string' ? sanitizeQuerySelector_1.sanitizeQuerySelector(title) : undefined}>
        {title && <panels_1.PanelHeader>{title}</panels_1.PanelHeader>}
        <panels_1.PanelBody>
          {typeof renderHeader === 'function' && renderHeader({ title: title, fields: fields })}

          {fields.map(function (field) {
                if (typeof field === 'function') {
                    return field();
                }
                var _ = field.defaultValue, fieldWithoutDefaultValue = tslib_1.__rest(field, ["defaultValue"]);
                // Allow the form panel disabled prop to override the fields
                // disabled prop, with fallback to the fields disabled state.
                if (disabled === true) {
                    fieldWithoutDefaultValue.disabled = true;
                    fieldWithoutDefaultValue.disabledReason = undefined;
                }
                return (<fieldFromConfig_1.default access={access} disabled={disabled} key={field.name} {...otherProps} {...additionalFieldProps} field={fieldWithoutDefaultValue} highlighted={_this.props.highlighted === "#" + field.name}/>);
            })}
          {typeof renderFooter === 'function' && renderFooter({ title: title, fields: fields })}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    FormPanel.defaultProps = {
        additionalFieldProps: {},
    };
    return FormPanel;
}(React.Component));
exports.default = FormPanel;
//# sourceMappingURL=formPanel.jsx.map