Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var indicator_1 = require("app/actionCreators/indicator");
var navigation_1 = require("app/actionCreators/navigation");
var autoComplete_1 = tslib_1.__importDefault(require("app/components/autoComplete"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var searchResult_1 = tslib_1.__importDefault(require("app/components/search/searchResult"));
var searchResultWrapper_1 = tslib_1.__importDefault(require("app/components/search/searchResultWrapper"));
var sources_1 = tslib_1.__importDefault(require("app/components/search/sources"));
var apiSource_1 = tslib_1.__importDefault(require("app/components/search/sources/apiSource"));
var commandSource_1 = tslib_1.__importDefault(require("app/components/search/sources/commandSource"));
var formSource_1 = tslib_1.__importDefault(require("app/components/search/sources/formSource"));
var routeSource_1 = tslib_1.__importDefault(require("app/components/search/sources/routeSource"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
// Not using typeof defaultProps because of the wrapping HOC which
// causes defaultProp magic to fall off.
var defaultProps = {
    renderItem: function (_a) {
        var item = _a.item, matches = _a.matches, itemProps = _a.itemProps, highlighted = _a.highlighted;
        return (<searchResultWrapper_1.default {...itemProps} highlighted={highlighted}>
      <searchResult_1.default highlighted={highlighted} item={item} matches={matches}/>
    </searchResultWrapper_1.default>);
    },
    sources: [apiSource_1.default, formSource_1.default, routeSource_1.default, commandSource_1.default],
    closeOnSelect: true,
};
// "Omni" search
var Search = /** @class */ (function (_super) {
    tslib_1.__extends(Search, _super);
    function Search() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSelect = function (item, state) {
            if (!item) {
                return;
            }
            analytics_1.trackAnalyticsEvent({
                eventKey: _this.props.entryPoint + ".select",
                eventName: _this.props.entryPoint + " Select",
                query: state && state.inputValue,
                result_type: item.resultType,
                source_type: item.sourceType,
                organization_id: null,
            });
            var to = item.to, action = item.action, configUrl = item.configUrl;
            // `action` refers to a callback function while
            // `to` is a react-router route
            if (action) {
                action(item, state);
                return;
            }
            if (!to) {
                return;
            }
            if (to.startsWith('http')) {
                var open_1 = window.open();
                if (open_1 === null) {
                    indicator_1.addErrorMessage(locale_1.t('Unable to open search result (a popup blocker may have caused this).'));
                    return;
                }
                open_1.opener = null;
                open_1.location.href = to;
                return;
            }
            var _a = _this.props, params = _a.params, router = _a.router;
            var nextPath = replaceRouterParams_1.default(to, params);
            navigation_1.navigateTo(nextPath, router, configUrl);
        };
        _this.saveQueryMetrics = debounce_1.default(function (query) {
            if (!query) {
                return;
            }
            analytics_1.trackAnalyticsEvent({
                eventKey: _this.props.entryPoint + ".query",
                eventName: _this.props.entryPoint + " Query",
                query: query,
                organization_id: null,
            });
        }, 200);
        _this.renderItem = function (_a) {
            var resultObj = _a.resultObj, index = _a.index, highlightedIndex = _a.highlightedIndex, getItemProps = _a.getItemProps;
            // resultObj is a fuse.js result object with {item, matches, score}
            var renderItem = _this.props.renderItem;
            var highlighted = index === highlightedIndex;
            var item = resultObj.item, matches = resultObj.matches;
            var key = item.title + "-" + index;
            var itemProps = tslib_1.__assign({}, getItemProps({
                item: item,
                index: index,
            }));
            if (typeof renderItem !== 'function') {
                throw new Error('Invalid `renderItem`');
            }
            var renderedItem = renderItem({
                item: item,
                matches: matches,
                index: index,
                highlighted: highlighted,
                itemProps: itemProps,
            });
            return React.cloneElement(renderedItem, { key: key });
        };
        return _this;
    }
    Search.prototype.componentDidMount = function () {
        analytics_1.trackAnalyticsEvent({
            eventKey: this.props.entryPoint + ".open",
            eventName: this.props.entryPoint + " Open",
            organization_id: null,
        });
    };
    Search.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, dropdownStyle = _a.dropdownStyle, searchOptions = _a.searchOptions, minSearch = _a.minSearch, maxResults = _a.maxResults, renderInput = _a.renderInput, sources = _a.sources, closeOnSelect = _a.closeOnSelect, resultFooter = _a.resultFooter;
        return (<autoComplete_1.default defaultHighlightedIndex={0} onSelect={this.handleSelect} closeOnSelect={closeOnSelect}>
        {function (_a) {
                var getInputProps = _a.getInputProps, getItemProps = _a.getItemProps, isOpen = _a.isOpen, inputValue = _a.inputValue, highlightedIndex = _a.highlightedIndex;
                var searchQuery = inputValue.toLowerCase().trim();
                var isValidSearch = inputValue.length >= minSearch;
                _this.saveQueryMetrics(searchQuery);
                return (<SearchWrapper>
              {renderInput({ getInputProps: getInputProps })}

              {isValidSearch && isOpen ? (<sources_1.default searchOptions={searchOptions} query={searchQuery} params={params} sources={sources !== null && sources !== void 0 ? sources : defaultProps.sources}>
                  {function (_a) {
                            var isLoading = _a.isLoading, results = _a.results, hasAnyResults = _a.hasAnyResults;
                            return (<DropdownBox className={dropdownStyle}>
                      {isLoading && (<LoadingWrapper>
                          <loadingIndicator_1.default mini hideMessage relative/>
                        </LoadingWrapper>)}
                      {!isLoading &&
                                    results.slice(0, maxResults).map(function (resultObj, index) {
                                        return _this.renderItem({
                                            resultObj: resultObj,
                                            index: index,
                                            highlightedIndex: highlightedIndex,
                                            getItemProps: getItemProps,
                                        });
                                    })}
                      {!isLoading && !hasAnyResults && (<EmptyItem>{locale_1.t('No results found')}</EmptyItem>)}
                      {!isLoading && resultFooter && (<ResultFooter>{resultFooter}</ResultFooter>)}
                    </DropdownBox>);
                        }}
                </sources_1.default>) : null}
            </SearchWrapper>);
            }}
      </autoComplete_1.default>);
    };
    Search.defaultProps = defaultProps;
    return Search;
}(React.Component));
exports.default = react_router_1.withRouter(Search);
var DropdownBox = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  box-shadow: ", ";\n  position: absolute;\n  top: 36px;\n  right: 0;\n  width: 400px;\n  border-radius: 5px;\n  overflow: auto;\n  max-height: 60vh;\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  box-shadow: ", ";\n  position: absolute;\n  top: 36px;\n  right: 0;\n  width: 400px;\n  border-radius: 5px;\n  overflow: auto;\n  max-height: 60vh;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowHeavy; });
var SearchWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ResultFooter = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: sticky;\n  bottom: 0;\n  left: 0;\n  right: 0;\n"], ["\n  position: sticky;\n  bottom: 0;\n  left: 0;\n  right: 0;\n"])));
var EmptyItem = styled_1.default(searchResultWrapper_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-align: center;\n  padding: 16px;\n  opacity: 0.5;\n"], ["\n  text-align: center;\n  padding: 16px;\n  opacity: 0.5;\n"])));
var LoadingWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  padding: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map