Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var selectAsyncControl_1 = tslib_1.__importDefault(require("./selectAsyncControl"));
var selectField_1 = tslib_1.__importDefault(require("./selectField"));
var SelectAsyncField = /** @class */ (function (_super) {
    tslib_1.__extends(SelectAsyncField, _super);
    function SelectAsyncField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onResults = function (data) {
            var name = _this.props.name;
            var results = data && data[name];
            return (results && results.map(function (_a) {
                var id = _a.id, text = _a.text;
                return ({ value: id, label: text });
            })) || [];
        };
        _this.onQuery = function (query) {
            // Used by legacy integrations
            return ({ autocomplete_query: query, autocomplete_field: _this.props.name });
        };
        return _this;
    }
    SelectAsyncField.prototype.getField = function () {
        // Callers should be able to override all props except onChange
        // FormField calls props.onChange via `setValue`
        return (<selectAsyncControl_1.default id={this.getId()} onResults={this.onResults} onQuery={this.onQuery} {...this.props} value={this.state.value} onChange={this.onChange}/>);
    };
    SelectAsyncField.defaultProps = tslib_1.__assign(tslib_1.__assign({}, selectField_1.default.defaultProps), { placeholder: 'Start typing to search for an issue' });
    return SelectAsyncField;
}(selectField_1.default));
exports.default = SelectAsyncField;
//# sourceMappingURL=selectAsyncField.jsx.map