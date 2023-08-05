Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var flatten_1 = tslib_1.__importDefault(require("lodash/flatten"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var marked_1 = require("app/utils/marked");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var defaultProps = {
    /**
     * Text used for the 'add' button. An empty string can be used
     * to just render the "+" icon.
     */
    addButtonText: locale_1.t('Add Item'),
    /**
     * Automatically save even if fields are empty
     */
    allowEmpty: false,
};
var TableField = /** @class */ (function (_super) {
    tslib_1.__extends(TableField, _super);
    function TableField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasValue = function (value) { return utils_1.defined(value) && !utils_1.objectIsEmpty(value); };
        _this.renderField = function (props) {
            var onChange = props.onChange, onBlur = props.onBlur, addButtonText = props.addButtonText, columnLabels = props.columnLabels, columnKeys = props.columnKeys, rawDisabled = props.disabled, allowEmpty = props.allowEmpty, confirmDeleteMessage = props.confirmDeleteMessage;
            var mappedKeys = columnKeys || [];
            var emptyValue = mappedKeys.reduce(function (a, v) {
                var _a;
                return (tslib_1.__assign(tslib_1.__assign({}, a), (_a = {}, _a[v] = null, _a)));
            }, { id: '' });
            var valueIsEmpty = _this.hasValue(props.value);
            var value = valueIsEmpty ? props.value : [];
            var saveChanges = function (nextValue) {
                onChange === null || onChange === void 0 ? void 0 : onChange(nextValue, []);
                // nextValue is an array of ObservableObjectAdministration objects
                var validValues = !flatten_1.default(Object.values(nextValue).map(Object.entries)).some(function (_a) {
                    var _b = tslib_1.__read(_a, 2), key = _b[0], val = _b[1];
                    return key !== 'id' && !val;
                } // don't allow empty values except if it's the ID field
                );
                if (allowEmpty || validValues) {
                    // TOOD: add debouncing or use a form save button
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur(nextValue, []);
                }
            };
            var addRow = function () {
                saveChanges(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(value)), [emptyValue]));
            };
            var removeRow = function (rowIndex) {
                var newValue = tslib_1.__spreadArray([], tslib_1.__read(value));
                newValue.splice(rowIndex, 1);
                saveChanges(newValue);
            };
            var setValue = function (rowIndex, fieldKey, fieldValue) {
                var newValue = tslib_1.__spreadArray([], tslib_1.__read(value));
                newValue[rowIndex][fieldKey] = fieldValue.currentTarget
                    ? fieldValue.currentTarget.value
                    : null;
                saveChanges(newValue);
            };
            // should not be a function for this component
            var disabled = typeof rawDisabled === 'function' ? false : rawDisabled;
            var button = (<button_1.default icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={addRow} size="xsmall" disabled={disabled}>
        {addButtonText}
      </button_1.default>);
            // The field will be set to inline when there is no value set for the
            // field, just show the button.
            if (!valueIsEmpty) {
                return <div>{button}</div>;
            }
            var renderConfirmMessage = function () {
                return (<React.Fragment>
          <alert_1.default type="error">
            <span dangerouslySetInnerHTML={{
                        __html: marked_1.singleLineRenderer(confirmDeleteMessage || locale_1.t('Are you sure you want to delete this item?')),
                    }}/>
          </alert_1.default>
        </React.Fragment>);
            };
            return (<React.Fragment>
        <HeaderContainer>
          {mappedKeys.map(function (fieldKey, i) { return (<Header key={fieldKey}>
              <HeaderLabel>{columnLabels === null || columnLabels === void 0 ? void 0 : columnLabels[fieldKey]}</HeaderLabel>
              {i === mappedKeys.length - 1 && button}
            </Header>); })}
        </HeaderContainer>
        {value.map(function (row, rowIndex) { return (<RowContainer data-test-id="field-row" key={rowIndex}>
            {mappedKeys.map(function (fieldKey, i) { return (<Row key={fieldKey}>
                <RowInput>
                  <input_1.default onChange={function (v) { return setValue(rowIndex, fieldKey, v); }} value={!utils_1.defined(row[fieldKey]) ? '' : row[fieldKey]}/>
                </RowInput>
                {i === mappedKeys.length - 1 && (<confirm_1.default priority="danger" disabled={disabled} onConfirm={function () { return removeRow(rowIndex); }} message={renderConfirmMessage()}>
                    <RemoveButton>
                      <button_1.default icon={<icons_1.IconDelete />} size="small" disabled={disabled} label={locale_1.t('delete')}/>
                    </RemoveButton>
                  </confirm_1.default>)}
              </Row>); })}
          </RowContainer>); })}
      </React.Fragment>);
        };
        return _this;
    }
    TableField.prototype.render = function () {
        var _this = this;
        // We need formatMessageValue=false since we're saving an object
        // and there isn't a great way to render the
        // change within the toast. Just turn off displaying the from/to portion of
        // the message
        return (<inputField_1.default {...this.props} formatMessageValue={false} inline={function (_a) {
            var model = _a.model;
            return !_this.hasValue(model.getValue(_this.props.name));
        }} field={this.renderField}/>);
    };
    TableField.defaultProps = defaultProps;
    return TableField;
}(React.Component));
exports.default = TableField;
var HeaderLabel = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"], ["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var HeaderContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var Header = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"])));
var RowContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-top: ", ";\n"])), space_1.default(1));
var Row = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  flex: 1 0 0;\n  align-items: center;\n  margin-top: ", ";\n"])), space_1.default(1));
var RowInput = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n"])), space_1.default(1));
var RemoveButton = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=tableField.jsx.map