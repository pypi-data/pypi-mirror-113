Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var iconReturn_1 = require("app/icons/iconReturn");
var locale_1 = require("app/locale");
var SubmitButton = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background: transparent;\n  box-shadow: none;\n  border: 1px solid transparent;\n  border-radius: ", ";\n  transition: 0.2s all;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 1.4em;\n  width: 1.4em;\n"], ["\n  background: transparent;\n  box-shadow: none;\n  border: 1px solid transparent;\n  border-radius: ", ";\n  transition: 0.2s all;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 1.4em;\n  width: 1.4em;\n"])), function (p) { return p.theme.borderRadius; });
var ClickTargetStyled = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n  width: 25%;\n  max-width: 2.5em;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n\n  &:hover ", " {\n    background: ", ";\n    box-shadow: ", ";\n    border: 1px solid ", ";\n  }\n"], ["\n  height: 100%;\n  width: 25%;\n  max-width: 2.5em;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n\n  &:hover ", " {\n    background: ", ";\n    box-shadow: ", ";\n    border: 1px solid ", ";\n  }\n"])), SubmitButton, function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; });
var ReturnButton = function (props) { return (<ClickTargetStyled {...props}>
    <tooltip_1.default title={locale_1.t('Save')}>
      <SubmitButton>
        <iconReturn_1.IconReturn />
      </SubmitButton>
    </tooltip_1.default>
  </ClickTargetStyled>); };
exports.default = ReturnButton;
var templateObject_1, templateObject_2;
//# sourceMappingURL=returnButton.jsx.map