Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var map_1 = tslib_1.__importDefault(require("lodash/map"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var iconClose_1 = require("app/icons/iconClose");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var stream_1 = require("app/utils/stream");
var tagFilter_1 = tslib_1.__importDefault(require("./tagFilter"));
var IssueListSidebar = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListSidebar, _super);
    function IssueListSidebar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            queryObj: stream_1.queryToObj(_this.props.query),
            textFilter: stream_1.queryToObj(_this.props.query).__text,
        };
        _this.onSelectTag = function (tag, value) {
            var newQuery = tslib_1.__assign({}, _this.state.queryObj);
            if (value) {
                newQuery[tag.key] = value;
            }
            else {
                delete newQuery[tag.key];
            }
            _this.setState({
                queryObj: newQuery,
            }, _this.onQueryChange);
        };
        _this.onTextChange = function (evt) {
            _this.setState({ textFilter: evt.target.value });
        };
        _this.onTextFilterSubmit = function (evt) {
            evt && evt.preventDefault();
            var newQueryObj = tslib_1.__assign(tslib_1.__assign({}, _this.state.queryObj), { __text: _this.state.textFilter });
            _this.setState({
                queryObj: newQueryObj,
            }, _this.onQueryChange);
        };
        _this.onQueryChange = function () {
            var query = stream_1.objToQuery(_this.state.queryObj);
            _this.props.onQueryChange && _this.props.onQueryChange(query);
        };
        _this.onClearSearch = function () {
            _this.setState({
                textFilter: '',
            }, _this.onTextFilterSubmit);
        };
        return _this;
    }
    IssueListSidebar.prototype.componentWillReceiveProps = function (nextProps) {
        // If query was updated by another source (e.g. SearchBar),
        // clobber state of sidebar with new query.
        var query = stream_1.objToQuery(this.state.queryObj);
        if (!isEqual_1.default(nextProps.query, query)) {
            var queryObj = stream_1.queryToObj(nextProps.query);
            this.setState({
                queryObj: queryObj,
                textFilter: queryObj.__text,
            });
        }
    };
    IssueListSidebar.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, tagValueLoader = _a.tagValueLoader, tags = _a.tags;
        return (<StreamSidebar>
        {loading ? (<loadingIndicator_1.default />) : (<React.Fragment>
            <StreamTagFilter>
              <StyledHeader>{locale_1.t('Text')}</StyledHeader>
              <form onSubmit={this.onTextFilterSubmit}>
                <input className="form-control" placeholder={locale_1.t('Search title and culprit text body')} onChange={this.onTextChange} value={this.state.textFilter}/>
                {this.state.textFilter && (<StyledIconClose size="xs" onClick={this.onClearSearch}/>)}
              </form>
              <StyledHr />
            </StreamTagFilter>

            {map_1.default(tags, function (tag) { return (<tagFilter_1.default value={_this.state.queryObj[tag.key]} key={tag.key} tag={tag} onSelect={_this.onSelectTag} tagValueLoader={tagValueLoader}/>); })}
          </React.Fragment>)}
      </StreamSidebar>);
    };
    IssueListSidebar.defaultProps = {
        tags: {},
        query: '',
        onQueryChange: function () { },
    };
    return IssueListSidebar;
}(React.Component));
exports.default = IssueListSidebar;
var StreamSidebar = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  width: 100%;\n"], ["\n  display: flex;\n  flex-direction: column;\n  width: 100%;\n"])));
var StyledIconClose = styled_1.default(iconClose_1.IconClose)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  position: absolute;\n  top: 13px;\n  right: 10px;\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  cursor: pointer;\n  position: absolute;\n  top: 13px;\n  right: 10px;\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
var StyledHeader = styled_1.default('h6')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space_1.default(1));
var StreamTagFilter = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var StyledHr = styled_1.default('hr')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0 0;\n"], ["\n  margin: ", " 0 0;\n"])), space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebar.jsx.map