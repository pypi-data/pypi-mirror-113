Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var inputField_1 = tslib_1.__importDefault(require("./inputField"));
function handleChangeDate(onChange, onBlur, date, close) {
    onChange(date);
    onBlur(date);
    // close dropdown menu
    close();
}
var Calendar = react_1.lazy(function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('./calendarField')); }); });
function DatePickerField(props) {
    return (<inputField_1.default {...props} field={function (_a) {
            var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, id = _a.id;
            var dateObj = new Date(value);
            var inputValue = !isNaN(dateObj.getTime()) ? dateObj : new Date();
            var dateString = moment_1.default(inputValue).format('LL');
            return (<dropdownMenu_1.default keepMenuOpen>
            {function (_a) {
                    var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps, actions = _a.actions;
                    return (<div {...getRootProps()}>
                <InputWrapper id={id} {...getActorProps()} isOpen={isOpen}>
                  <StyledInput readOnly value={dateString}/>
                  <CalendarIcon>
                    <icons_1.IconCalendar />
                  </CalendarIcon>
                </InputWrapper>

                {isOpen && (<CalendarMenu {...getMenuProps()}>
                    <react_1.Suspense fallback={<placeholder_1.default width="332px" height="282px">
                          <loadingIndicator_1.default />
                        </placeholder_1.default>}>
                      <Calendar date={inputValue} onChange={function (date) {
                                return handleChangeDate(onChange, onBlur, date, actions.close);
                            }}/>
                    </react_1.Suspense>
                  </CalendarMenu>)}
              </div>);
                }}
          </dropdownMenu_1.default>);
        }}/>);
}
exports.default = DatePickerField;
var InputWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n  cursor: text;\n  display: flex;\n  z-index: ", ";\n  ", "\n"], ["\n  ", "\n  cursor: text;\n  display: flex;\n  z-index: ", ";\n  ", "\n"])), input_1.inputStyles, function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; }, function (p) { return p.isOpen && 'border-bottom-left-radius: 0'; });
var StyledInput = styled_1.default('input')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border: none;\n  outline: none;\n  flex: 1;\n"], ["\n  border: none;\n  outline: none;\n  flex: 1;\n"])));
var CalendarMenu = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  background: ", ";\n  position: absolute;\n  left: 0;\n  border: 1px solid ", ";\n  border-top: none;\n  z-index: ", ";\n  margin-top: -1px;\n\n  .rdrMonthAndYearWrapper {\n    height: 50px;\n    padding-top: 0;\n  }\n"], ["\n  display: flex;\n  background: ", ";\n  position: absolute;\n  left: 0;\n  border: 1px solid ", ";\n  border-top: none;\n  z-index: ", ";\n  margin-top: -1px;\n\n  .rdrMonthAndYearWrapper {\n    height: 50px;\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.dropdownAutocomplete.menu; });
var CalendarIcon = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=datePickerField.jsx.map