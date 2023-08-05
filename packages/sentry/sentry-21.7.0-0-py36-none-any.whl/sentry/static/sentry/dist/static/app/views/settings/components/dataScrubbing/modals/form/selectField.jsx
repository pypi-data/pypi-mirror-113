Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SelectField = /** @class */ (function (_super) {
    tslib_1.__extends(SelectField, _super);
    function SelectField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // TODO(ts) The generics in react-select make getting a good type here hard.
        _this.selectRef = React.createRef();
        return _this;
    }
    SelectField.prototype.componentDidMount = function () {
        var _a, _b;
        if (!this.selectRef.current) {
            return;
        }
        if ((_b = (_a = this.selectRef.current) === null || _a === void 0 ? void 0 : _a.select) === null || _b === void 0 ? void 0 : _b.inputRef) {
            this.selectRef.current.select.inputRef.autocomplete = 'off';
        }
    };
    SelectField.prototype.render = function () {
        return (<selectControl_1.default {...this.props} isSearchable={false} styles={{
                control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { minHeight: '41px', height: '41px' })); },
            }} ref={this.selectRef} components={{
                Option: function (_a) {
                    var _b = _a.data, label = _b.label, description = _b.description, data = tslib_1.__rest(_b, ["label", "description"]), isSelected = _a.isSelected, props = tslib_1.__rest(_a, ["data", "isSelected"]);
                    return (<react_select_1.components.Option isSelected={isSelected} data={data} {...props}>
              <Wrapper>
                <div data-test-id="label">{label}</div>
                {description && <Description>{"(" + description + ")"}</Description>}
              </Wrapper>
            </react_select_1.components.Option>);
                },
            }} openOnFocus/>);
    };
    return SelectField;
}(React.Component));
exports.default = SelectField;
var Description = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  grid-gap: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=selectField.jsx.map