Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var savedSearches_1 = require("app/actionCreators/savedSearches");
var smartSearchBar_1 = tslib_1.__importDefault(require("app/components/smartSearchBar"));
var actions_1 = require("app/components/smartSearchBar/actions");
var types_1 = require("app/components/smartSearchBar/types");
var locale_1 = require("app/locale");
var types_2 = require("app/types");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var SEARCH_ITEMS = [
    {
        title: locale_1.t('Tag'),
        desc: 'browser:"Chrome 34", has:browser',
        value: 'browser:',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: locale_1.t('Status'),
        desc: 'is:resolved, unresolved, ignored, assigned, unassigned',
        value: 'is:',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: locale_1.t('Time or Count'),
        desc: 'firstSeen, lastSeen, event.timestamp, timesSeen',
        value: '',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: locale_1.t('Assigned'),
        desc: 'assigned, assigned_or_suggested:[me|[me, none]|user@example.com|#team-example]',
        value: '',
        type: types_1.ItemType.DEFAULT,
    },
    {
        title: locale_1.t('Bookmarked By'),
        desc: 'bookmarks:[me|user@example.com]',
        value: 'bookmarks:',
        type: types_1.ItemType.DEFAULT,
    },
];
var IssueListSearchBar = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListSearchBar, _super);
    function IssueListSearchBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            defaultSearchItems: [SEARCH_ITEMS, []],
            recentSearches: [],
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var resp;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.props.api.clear();
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 1:
                        resp = _a.sent();
                        this.setState({
                            defaultSearchItems: [
                                SEARCH_ITEMS,
                                resp
                                    ? resp.map(function (query) { return ({
                                        desc: query,
                                        value: query,
                                        type: types_1.ItemType.RECENT_SEARCH,
                                    }); })
                                    : [],
                            ],
                            recentSearches: resp,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * @returns array of tag values that substring match `query`
         */
        _this.getTagValues = function (tag, query) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var tagValueLoader, values;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        tagValueLoader = this.props.tagValueLoader;
                        return [4 /*yield*/, tagValueLoader(tag.key, query)];
                    case 1:
                        values = _a.sent();
                        return [2 /*return*/, values.map(function (_a) {
                                var value = _a.value;
                                return value;
                            })];
                }
            });
        }); };
        _this.getRecentSearches = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, recent;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, savedSearches_1.fetchRecentSearches(api, organization.slug, types_2.SavedSearchType.ISSUE)];
                    case 1:
                        recent = _c.sent();
                        return [2 /*return*/, (_b = recent === null || recent === void 0 ? void 0 : recent.map(function (_a) {
                                var query = _a.query;
                                return query;
                            })) !== null && _b !== void 0 ? _b : []];
                }
            });
        }); };
        _this.handleSavedRecentSearch = function () {
            // Reset recent searches
            _this.fetchData();
        };
        return _this;
    }
    IssueListSearchBar.prototype.componentDidMount = function () {
        // Ideally, we would fetch on demand (e.g. when input gets focus)
        // but `<SmartSearchBar>` is a bit complicated and this is the easiest route
        this.fetchData();
    };
    IssueListSearchBar.prototype.render = function () {
        var _a = this.props, _ = _a.tagValueLoader, savedSearch = _a.savedSearch, sort = _a.sort, onSidebarToggle = _a.onSidebarToggle, props = tslib_1.__rest(_a, ["tagValueLoader", "savedSearch", "sort", "onSidebarToggle"]);
        var pinnedSearch = (savedSearch === null || savedSearch === void 0 ? void 0 : savedSearch.isPinned) ? savedSearch : undefined;
        return (<smartSearchBar_1.default searchSource="main_search" hasRecentSearches maxSearchItems={5} savedSearchType={types_2.SavedSearchType.ISSUE} onGetTagValues={this.getTagValues} defaultSearchItems={this.state.defaultSearchItems} onSavedRecentSearch={this.handleSavedRecentSearch} actionBarItems={[
                actions_1.makePinSearchAction({ sort: sort, pinnedSearch: pinnedSearch }),
                actions_1.makeSaveSearchAction({ sort: sort }),
                actions_1.makeSearchBuilderAction({ onSidebarToggle: onSidebarToggle }),
            ]} {...props}/>);
    };
    return IssueListSearchBar;
}(React.Component));
exports.default = withApi_1.default(withOrganization_1.default(IssueListSearchBar));
//# sourceMappingURL=searchBar.jsx.map