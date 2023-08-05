Object.defineProperty(exports, "__esModule", { value: true });
exports.HelpSource = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var global_search_1 = require("@sentry-internal/global-search");
var dompurify_1 = tslib_1.__importDefault(require("dompurify"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var parseHtmlMarks_1 = tslib_1.__importDefault(require("app/utils/parseHtmlMarks"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var MARK_TAGS = {
    highlightPreTag: '<mark>',
    highlightPostTag: '</mark>',
};
var HelpSource = /** @class */ (function (_super) {
    tslib_1.__extends(HelpSource, _super);
    function HelpSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            results: [],
        };
        _this.search = new global_search_1.SentryGlobalSearch(['docs', 'help-center', 'develop', 'blog']);
        _this.doSearch = debounce_1.default(_this.unbouncedSearch, 300);
        return _this;
    }
    HelpSource.prototype.componentDidMount = function () {
        if (this.props.query !== undefined) {
            this.doSearch(this.props.query);
        }
    };
    HelpSource.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.query !== this.props.query) {
            this.doSearch(nextProps.query);
        }
    };
    HelpSource.prototype.unbouncedSearch = function (query) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, platforms, searchResults, results;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({ loading: true });
                        _a = this.props.platforms, platforms = _a === void 0 ? [] : _a;
                        return [4 /*yield*/, this.search.query(query, {
                                platforms: platforms.map(function (platform) { var _a; return (_a = global_search_1.standardSDKSlug(platform)) === null || _a === void 0 ? void 0 : _a.slug; }),
                            })];
                    case 1:
                        searchResults = _b.sent();
                        results = mapSearchResults(searchResults);
                        this.setState({ loading: false, results: results });
                        return [2 /*return*/];
                }
            });
        });
    };
    HelpSource.prototype.render = function () {
        return this.props.children({
            isLoading: this.state.loading,
            results: this.state.results,
        });
    };
    return HelpSource;
}(React.Component));
exports.HelpSource = HelpSource;
function mapSearchResults(results) {
    var items = [];
    results.forEach(function (section) {
        var sectionItems = section.hits.map(function (hit) {
            var _a, _b, _c;
            var title = parseHtmlMarks_1.default({
                key: 'title',
                htmlString: (_a = hit.title) !== null && _a !== void 0 ? _a : '',
                markTags: MARK_TAGS,
            });
            var description = parseHtmlMarks_1.default({
                key: 'description',
                htmlString: (_b = hit.text) !== null && _b !== void 0 ? _b : '',
                markTags: MARK_TAGS,
            });
            var item = tslib_1.__assign(tslib_1.__assign({}, hit), { sourceType: 'help', resultType: "help-" + hit.site, title: dompurify_1.default.sanitize((_c = hit.title) !== null && _c !== void 0 ? _c : ''), extra: hit.context.context1, description: hit.text ? dompurify_1.default.sanitize(hit.text) : undefined, to: hit.url });
            return { item: item, matches: [title, description], score: 1 };
        });
        // The first element should indicate the section.
        if (sectionItems.length > 0) {
            sectionItems[0].item.sectionHeading = section.name;
            sectionItems[0].item.sectionCount = sectionItems.length;
            items.push.apply(items, tslib_1.__spreadArray([], tslib_1.__read(sectionItems)));
            return;
        }
        // If we didn't have any results for this section mark it as empty
        var emptyHeaderItem = {
            sourceType: 'help',
            resultType: "help-" + section.site,
            title: "No results in " + section.name,
            sectionHeading: section.name,
            empty: true,
        };
        items.push({ item: emptyHeaderItem, score: 1 });
    });
    return items;
}
exports.default = withLatestContext_1.default(react_router_1.withRouter(HelpSource));
//# sourceMappingURL=helpSource.jsx.map