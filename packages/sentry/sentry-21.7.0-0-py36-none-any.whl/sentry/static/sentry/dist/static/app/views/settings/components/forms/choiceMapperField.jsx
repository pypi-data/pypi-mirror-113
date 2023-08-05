Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var defaultProps = {
    addButtonText: locale_1.t('Add Item'),
    perItemMapping: false,
    allowEmpty: false,
};
var ChoiceMapper = /** @class */ (function (_super) {
    tslib_1.__extends(ChoiceMapper, _super);
    function ChoiceMapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasValue = function (value) { return utils_1.defined(value) && !utils_1.objectIsEmpty(value); };
        _this.renderField = function (props) {
            var _a, _b, _c, _d;
            var onChange = props.onChange, onBlur = props.onBlur, addButtonText = props.addButtonText, addDropdown = props.addDropdown, mappedColumnLabel = props.mappedColumnLabel, columnLabels = props.columnLabels, mappedSelectors = props.mappedSelectors, perItemMapping = props.perItemMapping, disabled = props.disabled, allowEmpty = props.allowEmpty;
            var mappedKeys = Object.keys(columnLabels);
            var emptyValue = mappedKeys.reduce(function (a, v) {
                var _a;
                return (tslib_1.__assign(tslib_1.__assign({}, a), (_a = {}, _a[v] = null, _a)));
            }, {});
            var valueIsEmpty = _this.hasValue(props.value);
            var value = valueIsEmpty ? props.value : {};
            var saveChanges = function (nextValue) {
                onChange === null || onChange === void 0 ? void 0 : onChange(nextValue, {});
                var validValues = !Object.values(nextValue)
                    .map(function (o) { return Object.values(o).find(function (v) { return v === null; }); })
                    .includes(null);
                if (allowEmpty || validValues) {
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur();
                }
            };
            var addRow = function (data) {
                var _a;
                saveChanges(tslib_1.__assign(tslib_1.__assign({}, value), (_a = {}, _a[data.value] = emptyValue, _a)));
            };
            var removeRow = function (itemKey) {
                // eslint-disable-next-line no-unused-vars
                var _a = value, _b = itemKey, _ = _a[_b], updatedValue = tslib_1.__rest(_a, [typeof _b === "symbol" ? _b : _b + ""]);
                saveChanges(updatedValue);
            };
            var setValue = function (itemKey, fieldKey, fieldValue) {
                var _a, _b;
                saveChanges(tslib_1.__assign(tslib_1.__assign({}, value), (_a = {}, _a[itemKey] = tslib_1.__assign(tslib_1.__assign({}, value[itemKey]), (_b = {}, _b[fieldKey] = fieldValue, _b)), _a)));
            };
            // Remove already added values from the items list
            var selectableValues = (_b = (_a = addDropdown.items) === null || _a === void 0 ? void 0 : _a.filter(function (i) { return !value.hasOwnProperty(i.value); })) !== null && _b !== void 0 ? _b : [];
            var valueMap = (_d = (_c = addDropdown.items) === null || _c === void 0 ? void 0 : _c.reduce(function (map, item) {
                map[item.value] = item.label;
                return map;
            }, {})) !== null && _d !== void 0 ? _d : {};
            var dropdown = (<dropdownAutoComplete_1.default {...addDropdown} alignMenu={valueIsEmpty ? 'right' : 'left'} items={selectableValues} onSelect={addRow} disabled={disabled}>
        {function (_a) {
                    var isOpen = _a.isOpen;
                    return (<dropdownButton_1.default icon={<icons_1.IconAdd size="xs" isCircled/>} isOpen={isOpen} size="xsmall" disabled={disabled}>
            {addButtonText}
          </dropdownButton_1.default>);
                }}
      </dropdownAutoComplete_1.default>);
            // The field will be set to inline when there is no value set for the
            // field, just show the dropdown.
            if (!valueIsEmpty) {
                return <div>{dropdown}</div>;
            }
            return (<React.Fragment>
        <Header>
          <LabelColumn>
            <HeadingItem>{mappedColumnLabel}</HeadingItem>
          </LabelColumn>
          {mappedKeys.map(function (fieldKey, i) { return (<Heading key={fieldKey}>
              <HeadingItem>{columnLabels[fieldKey]}</HeadingItem>
              {i === mappedKeys.length - 1 && dropdown}
            </Heading>); })}
        </Header>
        {Object.keys(value).map(function (itemKey) { return (<Row key={itemKey}>
            <LabelColumn>{valueMap[itemKey]}</LabelColumn>
            {mappedKeys.map(function (fieldKey, i) { return (<Column key={fieldKey}>
                <Control>
                  <selectControl_1.default {...(perItemMapping
                        ? mappedSelectors[itemKey][fieldKey]
                        : mappedSelectors[fieldKey])} height={30} disabled={disabled} onChange={function (v) { return setValue(itemKey, fieldKey, v ? v.value : null); }} value={value[itemKey][fieldKey]}/>
                </Control>
                {i === mappedKeys.length - 1 && (<Actions>
                    <button_1.default icon={<icons_1.IconDelete />} size="small" disabled={disabled} onClick={function () { return removeRow(itemKey); }}/>
                  </Actions>)}
              </Column>); })}
          </Row>); })}
      </React.Fragment>);
        };
        return _this;
    }
    ChoiceMapper.prototype.render = function () {
        var _this = this;
        return (<inputField_1.default {...this.props} inline={function (_a) {
            var model = _a.model;
            return !_this.hasValue(model.getValue(_this.props.name));
        }} field={this.renderField}/>);
    };
    ChoiceMapper.defaultProps = defaultProps;
    return ChoiceMapper;
}(React.Component));
exports.default = ChoiceMapper;
var Header = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var Heading = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-left: ", ";\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  margin-left: ", ";\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"])), space_1.default(1));
var Row = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-top: ", ";\n  align-items: center;\n"], ["\n  display: flex;\n  margin-top: ", ";\n  align-items: center;\n"])), space_1.default(1));
var Column = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-left: ", ";\n  align-items: center;\n  flex: 1 0 0;\n"], ["\n  display: flex;\n  margin-left: ", ";\n  align-items: center;\n  flex: 1 0 0;\n"])), space_1.default(1));
var Control = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var LabelColumn = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 0 0 200px;\n"], ["\n  flex: 0 0 200px;\n"])));
var HeadingItem = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"], ["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Actions = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=choiceMapperField.jsx.map