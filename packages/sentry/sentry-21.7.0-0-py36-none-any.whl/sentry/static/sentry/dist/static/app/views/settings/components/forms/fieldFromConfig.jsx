Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var blankField_1 = tslib_1.__importDefault(require("./blankField"));
var booleanField_1 = tslib_1.__importDefault(require("./booleanField"));
var choiceMapperField_1 = tslib_1.__importDefault(require("./choiceMapperField"));
var emailField_1 = tslib_1.__importDefault(require("./emailField"));
var fieldSeparator_1 = tslib_1.__importDefault(require("./fieldSeparator"));
var hiddenField_1 = tslib_1.__importDefault(require("./hiddenField"));
var inputField_1 = tslib_1.__importDefault(require("./inputField"));
var numberField_1 = tslib_1.__importDefault(require("./numberField"));
var projectMapperField_1 = tslib_1.__importDefault(require("./projectMapperField"));
var radioField_1 = tslib_1.__importDefault(require("./radioField"));
var rangeField_1 = tslib_1.__importDefault(require("./rangeField"));
var richListField_1 = tslib_1.__importDefault(require("./richListField"));
var selectAsyncField_1 = tslib_1.__importDefault(require("./selectAsyncField"));
var selectField_1 = tslib_1.__importDefault(require("./selectField"));
var sentryProjectSelectorField_1 = tslib_1.__importDefault(require("./sentryProjectSelectorField"));
var tableField_1 = tslib_1.__importDefault(require("./tableField"));
var textareaField_1 = tslib_1.__importDefault(require("./textareaField"));
var textField_1 = tslib_1.__importDefault(require("./textField"));
var FieldFromConfig = /** @class */ (function (_super) {
    tslib_1.__extends(FieldFromConfig, _super);
    function FieldFromConfig() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FieldFromConfig.prototype.render = function () {
        var _a = this.props, field = _a.field, otherProps = tslib_1.__rest(_a, ["field"]);
        var props = tslib_1.__assign(tslib_1.__assign({}, otherProps), field);
        switch (field.type) {
            case 'separator':
                return <fieldSeparator_1.default />;
            case 'secret':
                return <inputField_1.default {...props} type="password"/>;
            case 'range':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <rangeField_1.default {...props}/>;
            case 'blank':
                return <blankField_1.default {...props}/>;
            case 'bool':
            case 'boolean':
                return <booleanField_1.default {...props}/>;
            case 'email':
                return <emailField_1.default {...props}/>;
            case 'hidden':
                return <hiddenField_1.default {...props}/>;
            case 'string':
            case 'text':
            case 'url':
                if (props.multiline) {
                    return <textareaField_1.default {...props}/>;
                }
                return <textField_1.default {...props}/>;
            case 'number':
                return <numberField_1.default {...props}/>;
            case 'textarea':
                return <textareaField_1.default {...props}/>;
            case 'choice':
            case 'select':
            case 'array':
                return <selectField_1.default {...props}/>;
            case 'choice_mapper':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <choiceMapperField_1.default {...props}/>;
            case 'radio':
                var choices = props.choices;
                if (!Array.isArray(choices)) {
                    throw new Error('Invalid `choices` type. Use an array of options');
                }
                return <radioField_1.default {...props} choices={choices}/>;
            case 'rich_list':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <richListField_1.default {...props}/>;
            case 'table':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <tableField_1.default {...props}/>;
            case 'project_mapper':
                return <projectMapperField_1.default {...props}/>;
            case 'sentry_project_selector':
                return <sentryProjectSelectorField_1.default {...props}/>;
            case 'select_async':
                return <selectAsyncField_1.default {...props}/>;
            case 'custom':
                return field.Component(props);
            default:
                return null;
        }
    };
    return FieldFromConfig;
}(react_1.Component));
exports.default = FieldFromConfig;
//# sourceMappingURL=fieldFromConfig.jsx.map