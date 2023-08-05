Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var defaultProps = {
    value: '',
};
var IssueListTagFilter = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListTagFilter, _super);
    function IssueListTagFilter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: '',
            isLoading: false,
            value: _this.props.value,
            textValue: _this.props.value,
        };
        _this.api = new api_1.Client();
        _this.handleLoadOptions = function () {
            var _a = _this.props, tag = _a.tag, tagValueLoader = _a.tagValueLoader;
            var textValue = _this.state.textValue;
            if (tag.isInput || tag.predefined) {
                return;
            }
            if (!_this.api) {
                return;
            }
            _this.setState({
                isLoading: true,
            });
            tagValueLoader(tag.key, textValue)
                .then(function (resp) {
                _this.setState({
                    isLoading: false,
                    options: Object.values(resp).map(function (_a) {
                        var value = _a.value;
                        return ({
                            value: value,
                            label: value,
                        });
                    }),
                });
            })
                .catch(function () {
                // TODO(billy): This endpoint seems to timeout a lot,
                // should we log these errors into datadog?
                indicator_1.addErrorMessage(locale_1.tct('Unable to retrieve values for tag [tagName]', {
                    tagName: textValue,
                }));
            });
        };
        _this.handleChangeInput = function (e) {
            var value = e.target.value;
            _this.setState({
                textValue: value,
            });
            _this.debouncedTextChange(value);
        };
        _this.debouncedTextChange = debounce_1.default(function (text) {
            _this.handleChange(text);
        }, 150);
        _this.handleOpenMenu = function () {
            if (_this.props.tag.predefined) {
                return;
            }
            _this.setState({
                isLoading: true,
            }, _this.handleLoadOptions);
        };
        _this.handleChangeSelect = function (valueObj) {
            var value = valueObj ? valueObj.value : null;
            _this.handleChange(value);
        };
        _this.handleChangeSelectInput = function (value) {
            _this.setState({
                textValue: value,
            }, _this.handleLoadOptions);
        };
        _this.handleChange = function (value) {
            var _a = _this.props, onSelect = _a.onSelect, tag = _a.tag;
            _this.setState({
                value: value,
            }, function () {
                onSelect && onSelect(tag, value);
            });
        };
        return _this;
    }
    IssueListTagFilter.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (nextProps.value !== this.state.value) {
            this.setState({
                value: nextProps.value,
                textValue: nextProps.value,
            });
        }
    };
    IssueListTagFilter.prototype.componentWillUnmount = function () {
        if (!this.api) {
            return;
        }
        this.api.clear();
    };
    IssueListTagFilter.prototype.render = function () {
        var tag = this.props.tag;
        var _a = this.state, options = _a.options, isLoading = _a.isLoading;
        return (<StreamTagFilter>
        <StyledHeader>{tag.key}</StyledHeader>

        {!!tag.isInput && (<input className="form-control" type="text" value={this.state.textValue} onChange={this.handleChangeInput}/>)}

        {!tag.isInput && (<selectControl_1.default clearable aria-label={tag.key} placeholder="--" loadingMessage={function () { return locale_1.t('Loading\u2026'); }} value={this.state.value} onChange={this.handleChangeSelect} isLoading={isLoading} onInputChange={this.handleChangeSelectInput} onFocus={this.handleOpenMenu} noResultsText={isLoading ? locale_1.t('Loading\u2026') : locale_1.t('No results found')} options={tag.predefined
                    ? tag.values &&
                        tag.values.map(function (value) { return ({
                            value: value,
                            label: value,
                        }); })
                    : options}/>)}
      </StreamTagFilter>);
    };
    IssueListTagFilter.defaultProps = defaultProps;
    return IssueListTagFilter;
}(React.Component));
exports.default = IssueListTagFilter;
var StreamTagFilter = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var StyledHeader = styled_1.default('h6')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=tagFilter.jsx.map