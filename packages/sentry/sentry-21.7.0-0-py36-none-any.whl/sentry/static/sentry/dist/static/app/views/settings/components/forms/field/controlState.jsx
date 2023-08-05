Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var animations_1 = require("app/styles/animations");
var spinner_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/spinner"));
/**
 * ControlState (i.e. loading/error icons) for form fields
 */
var ControlState = function (_a) {
    var isSaving = _a.isSaving, isSaved = _a.isSaved, error = _a.error;
    return (<react_1.Fragment>
    {isSaving ? (<ControlStateWrapper>
        <FormSpinner />
      </ControlStateWrapper>) : isSaved ? (<ControlStateWrapper>
        <FieldIsSaved>
          <icons_1.IconCheckmark size="18px"/>
        </FieldIsSaved>
      </ControlStateWrapper>) : null}

    {error ? (<ControlStateWrapper>
        <FieldError>
          <icons_1.IconWarning size="18px"/>
        </FieldError>
      </ControlStateWrapper>) : null}
  </react_1.Fragment>);
};
var ControlStateWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  line-height: 0;\n  padding: 0 8px;\n"], ["\n  line-height: 0;\n  padding: 0 8px;\n"])));
var FieldIsSaved = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  animation: ", " 0.3s ease 2s 1 forwards;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  color: ", ";\n  animation: ", " 0.3s ease 2s 1 forwards;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return p.theme.green300; }, animations_1.fadeOut);
var FormSpinner = styled_1.default(spinner_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: 0;\n"], ["\n  margin-left: 0;\n"])));
var FieldError = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  animation: ", " 1s ease infinite;\n"], ["\n  color: ", ";\n  animation: ", " 1s ease infinite;\n"])), function (p) { return p.theme.red300; }, function () { return animations_1.pulse(1.15); });
exports.default = ControlState;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=controlState.jsx.map