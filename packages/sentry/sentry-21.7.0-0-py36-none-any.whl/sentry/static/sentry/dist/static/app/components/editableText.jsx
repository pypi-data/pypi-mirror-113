Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var iconEdit_1 = require("app/icons/iconEdit");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var useKeyPress_1 = tslib_1.__importDefault(require("app/utils/useKeyPress"));
var useOnClickOutside_1 = tslib_1.__importDefault(require("app/utils/useOnClickOutside"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
function EditableText(_a) {
    var value = _a.value, onChange = _a.onChange, name = _a.name, errorMessage = _a.errorMessage, successMessage = _a.successMessage, _b = _a.isDisabled, isDisabled = _b === void 0 ? false : _b;
    var _c = tslib_1.__read(react_1.useState(false), 2), isEditing = _c[0], setIsEditing = _c[1];
    var _d = tslib_1.__read(react_1.useState(value), 2), inputValue = _d[0], setInputValue = _d[1];
    var isEmpty = !inputValue.trim();
    var innerWrapperRef = react_1.useRef(null);
    var labelRef = react_1.useRef(null);
    var inputRef = react_1.useRef(null);
    var enter = useKeyPress_1.default('Enter');
    var esc = useKeyPress_1.default('Escape');
    function revertValueAndCloseEditor() {
        if (value !== inputValue) {
            setInputValue(value);
        }
        if (isEditing) {
            setIsEditing(false);
        }
    }
    // check to see if the user clicked outside of this component
    useOnClickOutside_1.default(innerWrapperRef, function () {
        if (isEditing) {
            if (isEmpty) {
                displayStatusMessage('error');
                return;
            }
            if (inputValue !== value) {
                onChange(inputValue);
                displayStatusMessage('success');
            }
            setIsEditing(false);
        }
    });
    var onEnter = react_1.useCallback(function () {
        if (enter) {
            if (isEmpty) {
                displayStatusMessage('error');
                return;
            }
            if (inputValue !== value) {
                onChange(inputValue);
                displayStatusMessage('success');
            }
            setIsEditing(false);
        }
    }, [enter, inputValue, onChange]);
    var onEsc = react_1.useCallback(function () {
        if (esc) {
            revertValueAndCloseEditor();
        }
    }, [esc]);
    react_1.useEffect(function () {
        revertValueAndCloseEditor();
    }, [isDisabled, value]);
    // focus the cursor in the input field on edit start
    react_1.useEffect(function () {
        if (isEditing) {
            var inputElement = inputRef.current;
            if (utils_1.defined(inputElement)) {
                inputElement.focus();
            }
        }
    }, [isEditing]);
    react_1.useEffect(function () {
        if (isEditing) {
            // if Enter is pressed, save the value and close the editor
            onEnter();
            // if Escape is pressed, revert the value and close the editor
            onEsc();
        }
    }, [onEnter, onEsc, isEditing]); // watch the Enter and Escape key presses
    function displayStatusMessage(status) {
        if (status === 'error') {
            if (errorMessage) {
                indicator_1.addErrorMessage(errorMessage);
            }
            return;
        }
        if (successMessage) {
            indicator_1.addSuccessMessage(successMessage);
        }
    }
    function handleInputChange(event) {
        setInputValue(event.target.value);
    }
    function handleEditClick() {
        setIsEditing(true);
    }
    return (<Wrapper isDisabled={isDisabled} isEditing={isEditing}>
      {isEditing ? (<InputWrapper ref={innerWrapperRef} isEmpty={isEmpty} data-test-id="editable-text-input">
          <StyledInput name={name} ref={inputRef} value={inputValue} onChange={handleInputChange}/>
          <InputLabel>{inputValue}</InputLabel>
        </InputWrapper>) : (<Label onClick={isDisabled ? undefined : handleEditClick} ref={labelRef} data-test-id="editable-text-label">
          <InnerLabel>{inputValue}</InnerLabel>
          {!isDisabled && <iconEdit_1.IconEdit />}
        </Label>)}
    </Wrapper>);
}
exports.default = EditableText;
var Label = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n  cursor: pointer;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n  cursor: pointer;\n"])), space_1.default(1));
var InnerLabel = styled_1.default(textOverflow_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid transparent;\n  border-bottom: 1px dotted ", ";\n"], ["\n  border-top: 1px solid transparent;\n  border-bottom: 1px dotted ", ";\n"])), function (p) { return p.theme.gray200; });
var InputWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  background: ", ";\n  border-radius: ", ";\n  margin: -", " -", ";\n  max-width: calc(100% + ", ");\n"], ["\n  display: inline-block;\n  background: ", ";\n  border-radius: ", ";\n  margin: -", " -", ";\n  max-width: calc(100% + ", ");\n"])), function (p) { return p.theme.gray100; }, function (p) { return p.theme.borderRadius; }, space_1.default(0.5), space_1.default(1), space_1.default(2));
var StyledInput = styled_1.default(input_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  border: none !important;\n  background: transparent;\n  height: auto;\n  min-height: 34px;\n  padding: ", " ", ";\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    box-shadow: none;\n  }\n"], ["\n  border: none !important;\n  background: transparent;\n  height: auto;\n  min-height: 34px;\n  padding: ", " ", ";\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    box-shadow: none;\n  }\n"])), space_1.default(0.5), space_1.default(1));
var InputLabel = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  height: 0;\n  opacity: 0;\n  white-space: pre;\n  padding: 0 ", ";\n"], ["\n  height: 0;\n  opacity: 0;\n  white-space: pre;\n  padding: 0 ", ";\n"])), space_1.default(1));
var Wrapper = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: flex;\n\n  ", "\n"], ["\n  display: flex;\n\n  ", "\n"])), function (p) {
    return p.isDisabled &&
        "\n      " + InnerLabel + " {\n        border-bottom-color: transparent;\n      }\n    ";
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=editableText.jsx.map