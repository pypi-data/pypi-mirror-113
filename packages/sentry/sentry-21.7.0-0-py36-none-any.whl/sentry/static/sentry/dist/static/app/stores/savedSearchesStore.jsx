Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var findIndex_1 = tslib_1.__importDefault(require("lodash/findIndex"));
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var savedSearchesActions_1 = tslib_1.__importDefault(require("app/actions/savedSearchesActions"));
var savedSearchesStoreConfig = {
    state: {
        savedSearches: [],
        hasError: false,
        isLoading: true,
    },
    init: function () {
        var startFetchSavedSearches = savedSearchesActions_1.default.startFetchSavedSearches, fetchSavedSearchesSuccess = savedSearchesActions_1.default.fetchSavedSearchesSuccess, fetchSavedSearchesError = savedSearchesActions_1.default.fetchSavedSearchesError, createSavedSearchSuccess = savedSearchesActions_1.default.createSavedSearchSuccess, deleteSavedSearchSuccess = savedSearchesActions_1.default.deleteSavedSearchSuccess, pinSearch = savedSearchesActions_1.default.pinSearch, pinSearchSuccess = savedSearchesActions_1.default.pinSearchSuccess, resetSavedSearches = savedSearchesActions_1.default.resetSavedSearches, unpinSearch = savedSearchesActions_1.default.unpinSearch;
        this.listenTo(startFetchSavedSearches, this.onStartFetchSavedSearches);
        this.listenTo(fetchSavedSearchesSuccess, this.onFetchSavedSearchesSuccess);
        this.listenTo(fetchSavedSearchesError, this.onFetchSavedSearchesError);
        this.listenTo(resetSavedSearches, this.onReset);
        this.listenTo(createSavedSearchSuccess, this.onCreateSavedSearchSuccess);
        this.listenTo(deleteSavedSearchSuccess, this.onDeleteSavedSearchSuccess);
        this.listenTo(pinSearch, this.onPinSearch);
        this.listenTo(pinSearchSuccess, this.onPinSearchSuccess);
        this.listenTo(unpinSearch, this.onUnpinSearch);
        this.reset();
    },
    reset: function () {
        this.state = {
            savedSearches: [],
            hasError: false,
            isLoading: true,
        };
    },
    get: function () {
        return this.state;
    },
    /**
     * If pinned search, remove from list if user created pin (e.g. not org saved search and not global)
     * Otherwise change `isPinned` to false (e.g. if it's default or org saved search)
     */
    getFilteredSearches: function (type, existingSearchId) {
        return this.state.savedSearches
            .filter(function (savedSearch) {
            return !(savedSearch.isPinned &&
                savedSearch.type === type &&
                !savedSearch.isOrgCustom &&
                !savedSearch.isGlobal &&
                savedSearch.id !== existingSearchId);
        })
            .map(function (savedSearch) {
            if (typeof existingSearchId !== 'undefined' &&
                existingSearchId === savedSearch.id) {
                // Do not update existing search
                return savedSearch;
            }
            return tslib_1.__assign(tslib_1.__assign({}, savedSearch), { isPinned: false });
        });
    },
    updateExistingSearch: function (id, updateObj) {
        var index = findIndex_1.default(this.state.savedSearches, function (savedSearch) { return savedSearch.id === id; });
        if (index === -1) {
            return null;
        }
        var existingSavedSearch = this.state.savedSearches[index];
        var newSavedSearch = tslib_1.__assign(tslib_1.__assign({}, existingSavedSearch), updateObj);
        this.state.savedSearches[index] = newSavedSearch;
        return newSavedSearch;
    },
    /**
     * Find saved search by query string
     */
    findByQuery: function (query, sort) {
        return this.state.savedSearches.find(function (savedSearch) { return query === savedSearch.query && sort === savedSearch.sort; });
    },
    /**
     * Reset store to initial state
     */
    onReset: function () {
        this.reset();
        this.trigger(this.state);
    },
    onStartFetchSavedSearches: function () {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { isLoading: true });
        this.trigger(this.state);
    },
    onFetchSavedSearchesSuccess: function (data) {
        if (!Array.isArray(data)) {
            data = [];
        }
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { savedSearches: data, isLoading: false });
        this.trigger(this.state);
    },
    onFetchSavedSearchesError: function (_resp) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { savedSearches: [], isLoading: false, hasError: true });
        this.trigger(this.state);
    },
    onCreateSavedSearchSuccess: function (resp) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { savedSearches: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.state.savedSearches)), [resp]) });
        this.trigger(this.state);
    },
    onDeleteSavedSearchSuccess: function (search) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { savedSearches: this.state.savedSearches.filter(function (item) { return item.id !== search.id; }) });
        this.trigger(this.state);
    },
    onPinSearch: function (type, query, sort) {
        var existingSearch = this.findByQuery(query, sort);
        if (existingSearch) {
            this.updateExistingSearch(existingSearch.id, { isPinned: true });
        }
        var newPinnedSearch = !existingSearch
            ? [
                {
                    id: null,
                    name: 'My Pinned Search',
                    type: type,
                    query: query,
                    sort: sort,
                    isPinned: true,
                },
            ]
            : [];
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { savedSearches: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(newPinnedSearch)), tslib_1.__read(this.getFilteredSearches(type, existingSearch && existingSearch.id))) });
        this.trigger(this.state);
    },
    onPinSearchSuccess: function (resp) {
        var existingSearch = this.findByQuery(resp.query, resp.sort);
        if (existingSearch) {
            this.updateExistingSearch(existingSearch.id, resp);
        }
        this.trigger(this.state);
    },
    onUnpinSearch: function (type) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { 
            // Design decision that there can only be 1 pinned search per `type`
            savedSearches: this.getFilteredSearches(type) });
        this.trigger(this.state);
    },
};
var SavedSearchesStore = reflux_1.default.createStore(savedSearchesStoreConfig);
exports.default = SavedSearchesStore;
//# sourceMappingURL=savedSearchesStore.jsx.map