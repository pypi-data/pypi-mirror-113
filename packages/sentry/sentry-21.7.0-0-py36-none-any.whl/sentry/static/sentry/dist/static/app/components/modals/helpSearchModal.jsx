Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var helpSearch_1 = tslib_1.__importDefault(require("app/components/helpSearch"));
var hook_1 = tslib_1.__importDefault(require("app/components/hook"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var HelpSearchModal = function (_a) {
    var Body = _a.Body, closeModal = _a.closeModal, theme = _a.theme, organization = _a.organization, _b = _a.placeholder, placeholder = _b === void 0 ? locale_1.t('Search for documentation, FAQs, blog posts...') : _b, props = tslib_1.__rest(_a, ["Body", "closeModal", "theme", "organization", "placeholder"]);
    return (<Body>
    <react_1.ClassNames>
      {function (_a) {
            var injectedCss = _a.css;
            return (<helpSearch_1.default {...props} entryPoint="sidebar_help" dropdownStyle={injectedCss(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "], ["\n                width: 100%;\n                border: transparent;\n                border-top-left-radius: 0;\n                border-top-right-radius: 0;\n                position: initial;\n                box-shadow: none;\n                border-top: 1px solid ", ";\n              "])), theme.border)} renderInput={function (_a) {
                    var getInputProps = _a.getInputProps;
                    return (<InputWrapper>
              <Input autoFocus {...getInputProps({ type: 'text', label: placeholder, placeholder: placeholder })}/>
            </InputWrapper>);
                }} resultFooter={<hook_1.default name="help-modal:footer" {...{ organization: organization, closeModal: closeModal }}/>}/>);
        }}
    </react_1.ClassNames>
  </Body>);
};
var InputWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(0.25));
var Input = styled_1.default('input')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  padding: ", ";\n  border: none;\n  border-radius: 8px;\n  outline: none;\n\n  &:focus {\n    outline: none;\n  }\n"], ["\n  width: 100%;\n  padding: ", ";\n  border: none;\n  border-radius: 8px;\n  outline: none;\n\n  &:focus {\n    outline: none;\n  }\n"])), space_1.default(1));
exports.modalCss = react_1.css(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  [role='document'] {\n    padding: 0;\n  }\n"], ["\n  [role='document'] {\n    padding: 0;\n  }\n"])));
exports.default = react_1.withTheme(withOrganization_1.default(HelpSearchModal));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=helpSearchModal.jsx.map