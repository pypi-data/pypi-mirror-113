Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var savedSearchesStore_1 = tslib_1.__importDefault(require("app/stores/savedSearchesStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Wrap a component with saved issue search data from the store.
 */
function withSavedSearches(WrappedComponent) {
    var WithSavedSearches = /** @class */ (function (_super) {
        tslib_1.__extends(WithSavedSearches, _super);
        function WithSavedSearches() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = savedSearchesStore_1.default.get();
            _this.unsubscribe = savedSearchesStore_1.default.listen(function (searchesState) { return _this.onUpdate(searchesState); }, undefined);
            return _this;
        }
        WithSavedSearches.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithSavedSearches.prototype.onUpdate = function (newState) {
            this.setState(newState);
        };
        WithSavedSearches.prototype.render = function () {
            var _a = this.props, params = _a.params, location = _a.location, savedSearchLoading = _a.savedSearchLoading, savedSearchProp = _a.savedSearch, savedSearchesProp = _a.savedSearches;
            var searchId = params.searchId;
            var _b = this.state, savedSearches = _b.savedSearches, isLoading = _b.isLoading;
            var savedSearch = null;
            // Switch to the current saved search or pinned result if available
            if (!isLoading && savedSearches) {
                if (searchId) {
                    var match = savedSearches.find(function (search) { return search.id === searchId; });
                    savedSearch = match ? match : null;
                }
                // If there's no direct saved search being requested (via URL route)
                // *AND* there's no query in URL, then check if there is pinned search
                //
                // Note: Don't use pinned searches when there is an empty query (query === empty string)
                if (!savedSearch && typeof location.query.query === 'undefined') {
                    var pin = savedSearches.find(function (search) { return search.isPinned; });
                    savedSearch = pin ? pin : null;
                }
            }
            return (<WrappedComponent {...this.props} savedSearches={savedSearchesProp !== null && savedSearchesProp !== void 0 ? savedSearchesProp : savedSearches} savedSearchLoading={savedSearchLoading !== null && savedSearchLoading !== void 0 ? savedSearchLoading : isLoading} savedSearch={savedSearchProp !== null && savedSearchProp !== void 0 ? savedSearchProp : savedSearch}/>);
        };
        WithSavedSearches.displayName = "withSavedSearches(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithSavedSearches;
    }(React.Component));
    return WithSavedSearches;
}
exports.default = withSavedSearches;
//# sourceMappingURL=withSavedSearches.jsx.map