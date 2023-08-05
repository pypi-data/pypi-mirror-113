Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var booleanField_1 = tslib_1.__importDefault(require("app/components/forms/booleanField"));
var emailField_1 = tslib_1.__importDefault(require("app/components/forms/emailField"));
var numberField_1 = tslib_1.__importDefault(require("app/components/forms/numberField"));
var passwordField_1 = tslib_1.__importDefault(require("app/components/forms/passwordField"));
var selectAsyncField_1 = tslib_1.__importDefault(require("app/components/forms/selectAsyncField"));
var selectCreatableField_1 = tslib_1.__importDefault(require("app/components/forms/selectCreatableField"));
var selectField_1 = tslib_1.__importDefault(require("app/components/forms/selectField"));
var textareaField_1 = tslib_1.__importDefault(require("app/components/forms/textareaField"));
var textField_1 = tslib_1.__importDefault(require("app/components/forms/textField"));
var utils_1 = require("app/utils");
var GenericField = function (_a) {
    var config = _a.config, _b = _a.formData, formData = _b === void 0 ? {} : _b, _c = _a.formErrors, formErrors = _c === void 0 ? {} : _c, formState = _a.formState, onChange = _a.onChange;
    var required = utils_1.defined(config.required) ? config.required : true;
    var fieldProps = tslib_1.__assign(tslib_1.__assign({}, config), { value: formData[config.name], onChange: onChange, label: config.label + (required ? '*' : ''), placeholder: config.placeholder, required: required, name: config.name, error: (formErrors || {})[config.name], defaultValue: config.default, disabled: config.readonly, key: config.name, formState: formState, help: utils_1.defined(config.help) && config.help !== '' ? (<span dangerouslySetInnerHTML={{ __html: config.help }}/>) : null });
    switch (config.type) {
        case 'secret':
            return <passwordField_1.default {...fieldProps}/>;
        case 'bool':
            return <booleanField_1.default {...fieldProps}/>;
        case 'email':
            return <emailField_1.default {...fieldProps}/>;
        case 'string':
        case 'text':
        case 'url':
            if (fieldProps.choices) {
                return <selectCreatableField_1.default {...fieldProps}/>;
            }
            return <textField_1.default {...fieldProps}/>;
        case 'number':
            return <numberField_1.default {...fieldProps}/>;
        case 'textarea':
            return <textareaField_1.default {...fieldProps}/>;
        case 'choice':
        case 'select':
            // the chrome required tip winds up in weird places
            // for select elements, so just make it look like
            // it's required (with *) and rely on server validation
            var _1 = fieldProps.required, selectProps = tslib_1.__rest(fieldProps, ["required"]);
            if (config.has_autocomplete) {
                // Redeclaring field props here as config has been narrowed to include the correct options for SelectAsyncField
                var selectFieldProps = tslib_1.__assign(tslib_1.__assign({}, config), selectProps);
                return <selectAsyncField_1.default {...selectFieldProps}/>;
            }
            return <selectField_1.default {...selectProps}/>;
        default:
            return null;
    }
};
exports.default = GenericField;
//# sourceMappingURL=genericField.jsx.map