Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var iconClose_1 = require("app/icons/iconClose");
var locale_1 = require("app/locale");
var callIfFunction_1 = require("app/utils/callIfFunction");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var SearchBar = /** @class */ (function (_super) {
    tslib_1.__extends(SearchBar, _super);
    function SearchBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: _this.props.query || _this.props.defaultQuery,
            dropdownVisible: false,
        };
        _this.searchInputRef = React.createRef();
        _this.blur = function () {
            if (_this.searchInputRef.current) {
                _this.searchInputRef.current.blur();
            }
        };
        _this.onSubmit = function (evt) {
            evt.preventDefault();
            _this.blur();
            _this.props.onSearch(_this.state.query);
        };
        _this.clearSearch = function () {
            _this.setState({ query: _this.props.defaultQuery }, function () {
                _this.props.onSearch(_this.state.query);
                callIfFunction_1.callIfFunction(_this.props.onChange, _this.state.query);
            });
        };
        _this.onQueryFocus = function () {
            _this.setState({
                dropdownVisible: true,
            });
        };
        _this.onQueryBlur = function () {
            _this.setState({ dropdownVisible: false });
        };
        _this.onQueryChange = function (evt) {
            var value = evt.target.value;
            _this.setState({ query: value });
            callIfFunction_1.callIfFunction(_this.props.onChange, value);
        };
        return _this;
    }
    SearchBar.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (nextProps.query !== this.props.query) {
            this.setState({
                query: nextProps.query,
            });
        }
    };
    SearchBar.prototype.render = function () {
        var _a = this.props, className = _a.className, width = _a.width;
        return (<div className={classnames_1.default('search', className)}>
        <form className="form-horizontal" onSubmit={this.onSubmit}>
          <div>
            <StyledInput type="text" className="search-input" placeholder={this.props.placeholder} name="query" ref={this.searchInputRef} autoComplete="off" value={this.state.query} onBlur={this.onQueryBlur} onChange={this.onQueryChange} width={width}/>
            <StyledIconSearch className="search-input-icon" size="sm" color="gray300"/>
            {this.state.query !== this.props.defaultQuery && (<SearchClearButton type="button" className="search-clear-form" priority="link" onClick={this.clearSearch} size="xsmall" icon={<iconClose_1.IconClose />} label={locale_1.t('Clear')}/>)}
          </div>
        </form>
      </div>);
    };
    SearchBar.defaultProps = {
        query: '',
        defaultQuery: '',
        onSearch: function () { },
    };
    return SearchBar;
}(React.PureComponent));
var StyledInput = styled_1.default(input_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: ", ";\n  &.focus-visible {\n    box-shadow: inset 0 2px 0 rgba(0, 0, 0, 0.04), 0 0 6px rgba(177, 171, 225, 0.3);\n    border-color: #a598b2;\n    outline: none;\n  }\n"], ["\n  width: ", ";\n  &.focus-visible {\n    box-shadow: inset 0 2px 0 rgba(0, 0, 0, 0.04), 0 0 6px rgba(177, 171, 225, 0.3);\n    border-color: #a598b2;\n    outline: none;\n  }\n"])), function (p) { return (p.width ? p.width : undefined); });
var StyledIconSearch = styled_1.default(icons_1.IconSearch)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 50%;\n  transform: translateY(-50%);\n  left: 14px;\n"], ["\n  position: absolute;\n  top: 50%;\n  transform: translateY(-50%);\n  left: 14px;\n"])));
var SearchClearButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 50%;\n  height: 16px;\n  transform: translateY(-50%);\n  right: 10px;\n  font-size: ", ";\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  position: absolute;\n  top: 50%;\n  height: 16px;\n  transform: translateY(-50%);\n  right: 10px;\n  font-size: ", ";\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
exports.default = SearchBar;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=searchBar.jsx.map