Object.defineProperty(exports, "__esModule", { value: true });
exports.SmartSearchBar = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_autosize_textarea_1 = tslib_1.__importDefault(require("react-autosize-textarea"));
var react_router_1 = require("react-router");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var indicator_1 = require("app/actionCreators/indicator");
var savedSearches_1 = require("app/actionCreators/savedSearches");
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var parser_1 = require("app/components/searchSyntax/parser");
var renderer_1 = tslib_1.__importDefault(require("app/components/searchSyntax/renderer"));
var utils_1 = require("app/components/searchSyntax/utils");
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var callIfFunction_1 = require("app/utils/callIfFunction");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withExperiment_1 = tslib_1.__importDefault(require("app/utils/withExperiment"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var actions_1 = require("./actions");
var searchDropdown_1 = tslib_1.__importDefault(require("./searchDropdown"));
var types_2 = require("./types");
var utils_3 = require("./utils");
var DROPDOWN_BLUR_DURATION = 200;
/**
 * The max width in pixels of the search bar at which the buttons will
 * have overflowed into the dropdown.
 */
var ACTION_OVERFLOW_WIDTH = 400;
/**
 * Actions are moved to the overflow dropdown after each pixel step is reached.
 */
var ACTION_OVERFLOW_STEPS = 75;
/**
 * Is the SearchItem a default item
 */
var isDefaultDropdownItem = function (item) { return (item === null || item === void 0 ? void 0 : item.type) === types_2.ItemType.DEFAULT; };
var makeQueryState = function (query) { return ({
    query: query,
    parsedQuery: parser_1.parseSearch(query),
}); };
var generateOpAutocompleteGroup = function (validOps, tagName) {
    var operatorMap = utils_3.generateOperatorEntryMap(tagName);
    var operatorItems = validOps.map(function (op) { return operatorMap[op]; });
    return {
        searchItems: operatorItems,
        recentSearchItems: undefined,
        tagName: '',
        type: types_2.ItemType.TAG_OPERATOR,
    };
};
var SmartSearchBar = /** @class */ (function (_super) {
    tslib_1.__extends(SmartSearchBar, _super);
    function SmartSearchBar() {
        var _a, _b;
        var _this = _super.apply(this, tslib_1.__spreadArray([], tslib_1.__read(arguments))) || this;
        _this.state = {
            query: _this.initialQuery,
            parsedQuery: parser_1.parseSearch(_this.initialQuery),
            searchTerm: '',
            searchGroups: [],
            flatSearchItems: [],
            activeSearchItem: -1,
            tags: {},
            inputHasFocus: false,
            loading: false,
            numActionsVisible: (_b = (_a = _this.props.actionBarItems) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : 0,
        };
        /**
         * Ref to the search element itself
         */
        _this.searchInput = React.createRef();
        /**
         * Ref to the search container
         */
        _this.containerRef = React.createRef();
        /**
         * Used to determine when actions should be moved to the action overflow menu
         */
        _this.inputResizeObserver = null;
        /**
         * Updates the numActionsVisible count as the search bar is resized
         */
        _this.updateActionsVisible = function (entries) {
            var _a, _b;
            if (entries.length === 0) {
                return;
            }
            var entry = entries[0];
            var width = entry.contentRect.width;
            var actionCount = (_b = (_a = _this.props.actionBarItems) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : 0;
            var numActionsVisible = Math.min(actionCount, Math.floor(Math.max(0, width - ACTION_OVERFLOW_WIDTH) / ACTION_OVERFLOW_STEPS));
            if (_this.state.numActionsVisible === numActionsVisible) {
                return;
            }
            _this.setState({ numActionsVisible: numActionsVisible });
        };
        _this.onSubmit = function (evt) {
            evt.preventDefault();
            _this.doSearch();
        };
        _this.clearSearch = function () {
            return _this.setState(makeQueryState(''), function () {
                return callIfFunction_1.callIfFunction(_this.props.onSearch, _this.state.query);
            });
        };
        _this.onQueryFocus = function () { return _this.setState({ inputHasFocus: true }); };
        _this.onQueryBlur = function (e) {
            // wait before closing dropdown in case blur was a result of clicking a
            // menu option
            var value = e.target.value;
            var blurHandler = function () {
                _this.blurTimeout = undefined;
                _this.setState({ inputHasFocus: false });
                callIfFunction_1.callIfFunction(_this.props.onBlur, value);
            };
            _this.blurTimeout = window.setTimeout(blurHandler, DROPDOWN_BLUR_DURATION);
        };
        _this.onQueryChange = function (evt) {
            var query = evt.target.value.replace('\n', '');
            _this.setState(makeQueryState(query), _this.updateAutoCompleteItems);
            callIfFunction_1.callIfFunction(_this.props.onChange, evt.target.value, evt);
        };
        _this.onInputClick = function () { return _this.updateAutoCompleteItems(); };
        /**
         * Handle keyboard navigation
         */
        _this.onKeyDown = function (evt) {
            var _a, _b, _c;
            var onKeyDown = _this.props.onKeyDown;
            var key = evt.key;
            callIfFunction_1.callIfFunction(onKeyDown, evt);
            if (!_this.state.searchGroups.length) {
                return;
            }
            var isSelectingDropdownItems = _this.state.activeSearchItem !== -1;
            if (key === 'ArrowDown' || key === 'ArrowUp') {
                evt.preventDefault();
                var _d = _this.state, flatSearchItems = _d.flatSearchItems, activeSearchItem = _d.activeSearchItem;
                var searchGroups = tslib_1.__spreadArray([], tslib_1.__read(_this.state.searchGroups));
                var _e = tslib_1.__read(isSelectingDropdownItems
                    ? utils_3.filterSearchGroupsByIndex(searchGroups, activeSearchItem)
                    : [], 2), groupIndex = _e[0], childrenIndex = _e[1];
                // Remove the previous 'active' property
                if (typeof groupIndex !== 'undefined') {
                    if (childrenIndex !== undefined &&
                        ((_b = (_a = searchGroups[groupIndex]) === null || _a === void 0 ? void 0 : _a.children) === null || _b === void 0 ? void 0 : _b[childrenIndex])) {
                        delete searchGroups[groupIndex].children[childrenIndex].active;
                    }
                }
                var currIndex = isSelectingDropdownItems ? activeSearchItem : 0;
                var totalItems = flatSearchItems.length;
                // Move the selected index up/down
                var nextActiveSearchItem = key === 'ArrowUp'
                    ? (currIndex - 1 + totalItems) % totalItems
                    : isSelectingDropdownItems
                        ? (currIndex + 1) % totalItems
                        : 0;
                var _f = tslib_1.__read(utils_3.filterSearchGroupsByIndex(searchGroups, nextActiveSearchItem), 2), nextGroupIndex = _f[0], nextChildrenIndex = _f[1];
                // Make sure search items exist (e.g. both groups could be empty) and
                // attach the 'active' property to the item
                if (nextGroupIndex !== undefined &&
                    nextChildrenIndex !== undefined &&
                    ((_c = searchGroups[nextGroupIndex]) === null || _c === void 0 ? void 0 : _c.children)) {
                    searchGroups[nextGroupIndex].children[nextChildrenIndex] = tslib_1.__assign(tslib_1.__assign({}, searchGroups[nextGroupIndex].children[nextChildrenIndex]), { active: true });
                }
                _this.setState({ searchGroups: searchGroups, activeSearchItem: nextActiveSearchItem });
            }
            if ((key === 'Tab' || key === 'Enter') && isSelectingDropdownItems) {
                evt.preventDefault();
                var _g = _this.state, activeSearchItem = _g.activeSearchItem, searchGroups = _g.searchGroups;
                var _h = tslib_1.__read(utils_3.filterSearchGroupsByIndex(searchGroups, activeSearchItem), 2), groupIndex = _h[0], childrenIndex = _h[1];
                var item = groupIndex !== undefined &&
                    childrenIndex !== undefined &&
                    searchGroups[groupIndex].children[childrenIndex];
                if (item && !isDefaultDropdownItem(item)) {
                    _this.onAutoComplete(item.value, item);
                }
                return;
            }
            if (key === 'Enter' && !isSelectingDropdownItems) {
                _this.doSearch();
                return;
            }
        };
        _this.onKeyUp = function (evt) {
            if (evt.key === 'ArrowLeft' || evt.key === 'ArrowRight') {
                _this.updateAutoCompleteItems();
            }
            // Other keys are managed at onKeyDown function
            if (evt.key !== 'Escape') {
                return;
            }
            evt.preventDefault();
            var isSelectingDropdownItems = _this.state.activeSearchItem > -1;
            if (!isSelectingDropdownItems) {
                _this.blur();
                return;
            }
            var _a = _this.state, searchGroups = _a.searchGroups, activeSearchItem = _a.activeSearchItem;
            var _b = tslib_1.__read(isSelectingDropdownItems
                ? utils_3.filterSearchGroupsByIndex(searchGroups, activeSearchItem)
                : [], 2), groupIndex = _b[0], childrenIndex = _b[1];
            if (groupIndex !== undefined && childrenIndex !== undefined) {
                delete searchGroups[groupIndex].children[childrenIndex].active;
            }
            _this.setState({
                activeSearchItem: -1,
                searchGroups: tslib_1.__spreadArray([], tslib_1.__read(_this.state.searchGroups)),
            });
        };
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with data when ready
         */
        _this.getTagValues = debounce_1.default(function (tag, query) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var location, endpointParams, values, err_1, noValueQuery;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        // Strip double quotes if there are any
                        query = query.replace(/"/g, '').trim();
                        if (!this.props.onGetTagValues) {
                            return [2 /*return*/, []];
                        }
                        if (this.state.noValueQuery !== undefined &&
                            query.startsWith(this.state.noValueQuery)) {
                            return [2 /*return*/, []];
                        }
                        location = this.props.location;
                        endpointParams = getParams_1.getParams(location.query);
                        this.setState({ loading: true });
                        values = [];
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.onGetTagValues(tag, query, endpointParams)];
                    case 2:
                        values = _a.sent();
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.setState({ loading: false });
                        Sentry.captureException(err_1);
                        return [2 /*return*/, []];
                    case 4:
                        if (tag.key === 'release:' && !values.includes('latest')) {
                            values.unshift('latest');
                        }
                        noValueQuery = values.length === 0 && query.length > 0 ? query : undefined;
                        this.setState({ noValueQuery: noValueQuery });
                        return [2 /*return*/, values.map(function (value) {
                                // Wrap in quotes if there is a space
                                var escapedValue = value.includes(' ') || value.includes('"')
                                    ? "\"" + value.replace(/"/g, '\\"') + "\""
                                    : value;
                                return { value: escapedValue, desc: escapedValue, type: types_2.ItemType.TAG_VALUE };
                            })];
                }
            });
        }); }, constants_1.DEFAULT_DEBOUNCE_DURATION, { leading: true });
        /**
         * Returns array of tag values that substring match `query`; invokes `callback`
         * with results
         */
        _this.getPredefinedTagValues = function (tag, query) {
            var _a;
            return ((_a = tag.values) !== null && _a !== void 0 ? _a : [])
                .filter(function (value) { return value.indexOf(query) > -1; })
                .map(function (value, i) { return ({
                value: value,
                desc: value,
                type: types_2.ItemType.TAG_VALUE,
                ignoreMaxSearchItems: tag.maxSuggestedValues ? i < tag.maxSuggestedValues : false,
            }); });
        };
        /**
         * Get recent searches
         */
        _this.getRecentSearches = debounce_1.default(function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, savedSearchType, hasRecentSearches, onGetRecentSearches, fetchFn;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, savedSearchType = _a.savedSearchType, hasRecentSearches = _a.hasRecentSearches, onGetRecentSearches = _a.onGetRecentSearches;
                        // `savedSearchType` can be 0
                        if (!utils_2.defined(savedSearchType) || !hasRecentSearches) {
                            return [2 /*return*/, []];
                        }
                        fetchFn = onGetRecentSearches || this.fetchRecentSearches;
                        return [4 /*yield*/, fetchFn(this.state.query)];
                    case 1: return [2 /*return*/, _b.sent()];
                }
            });
        }); }, constants_1.DEFAULT_DEBOUNCE_DURATION, { leading: true });
        _this.fetchRecentSearches = function (fullQuery) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, savedSearchType, recentSearches, e_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, savedSearchType = _a.savedSearchType;
                        if (savedSearchType === undefined) {
                            return [2 /*return*/, []];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, savedSearches_1.fetchRecentSearches(api, organization.slug, savedSearchType, fullQuery)];
                    case 2:
                        recentSearches = _b.sent();
                        // If `recentSearches` is undefined or not an array, the function will
                        // return an array anyway
                        return [2 /*return*/, recentSearches.map(function (searches) { return ({
                                desc: searches.query,
                                value: searches.query,
                                type: types_2.ItemType.RECENT_SEARCH,
                            }); })];
                    case 3:
                        e_1 = _b.sent();
                        Sentry.captureException(e_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/, []];
                }
            });
        }); };
        _this.getReleases = debounce_1.default(function (tag, query) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var releasePromise, tags, tagValues, releases, releaseValues;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        releasePromise = this.fetchReleases(query);
                        tags = this.getPredefinedTagValues(tag, query);
                        tagValues = tags.map(function (v) { return (tslib_1.__assign(tslib_1.__assign({}, v), { type: types_2.ItemType.FIRST_RELEASE })); });
                        return [4 /*yield*/, releasePromise];
                    case 1:
                        releases = _a.sent();
                        releaseValues = releases.map(function (r) { return ({
                            value: r.shortVersion,
                            desc: r.shortVersion,
                            type: types_2.ItemType.FIRST_RELEASE,
                        }); });
                        return [2 /*return*/, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(tagValues)), tslib_1.__read(releaseValues))];
                }
            });
        }); }, constants_1.DEFAULT_DEBOUNCE_DURATION, { leading: true });
        /**
         * Fetches latest releases from a organization/project. Returns an empty array
         * if an error is encountered.
         */
        _this.fetchReleases = function (releaseVersion) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, location, organization, project, url, fetchQuery, e_2;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, location = _a.location, organization = _a.organization;
                        project = location && location.query ? location.query.projectId : undefined;
                        url = "/organizations/" + organization.slug + "/releases/";
                        fetchQuery = {
                            per_page: constants_1.MAX_AUTOCOMPLETE_RELEASES,
                        };
                        if (releaseVersion) {
                            fetchQuery.query = releaseVersion;
                        }
                        if (project) {
                            fetchQuery.project = project;
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(url, {
                                method: 'GET',
                                query: fetchQuery,
                            })];
                    case 2: return [2 /*return*/, _b.sent()];
                    case 3:
                        e_2 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to fetch releases'));
                        Sentry.captureException(e_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/, []];
                }
            });
        }); };
        _this.generateValueAutocompleteGroup = function (tagName, query) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, prepareQuery, excludeEnvironment, supportedTags, preparedQuery, filteredSearchGroups, tag, fetchTagValuesFn, _b, tagValues, recentSearches;
            var _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, prepareQuery = _a.prepareQuery, excludeEnvironment = _a.excludeEnvironment;
                        supportedTags = (_c = this.props.supportedTags) !== null && _c !== void 0 ? _c : {};
                        preparedQuery = typeof prepareQuery === 'function' ? prepareQuery(query) : query;
                        filteredSearchGroups = !preparedQuery
                            ? this.state.searchGroups
                            : this.state.searchGroups.filter(function (item) { return item.value && item.value.indexOf(preparedQuery) !== -1; });
                        this.setState({
                            searchTerm: query,
                            searchGroups: filteredSearchGroups,
                        });
                        tag = supportedTags[tagName];
                        if (!tag) {
                            return [2 /*return*/, {
                                    searchItems: [],
                                    recentSearchItems: [],
                                    tagName: tagName,
                                    type: types_2.ItemType.INVALID_TAG,
                                }];
                        }
                        // Ignore the environment tag if the feature is active and
                        // excludeEnvironment = true
                        if (excludeEnvironment && tagName === 'environment') {
                            return [2 /*return*/, null];
                        }
                        fetchTagValuesFn = tag.key === 'firstRelease'
                            ? this.getReleases
                            : tag.predefined
                                ? this.getPredefinedTagValues
                                : this.getTagValues;
                        return [4 /*yield*/, Promise.all([
                                fetchTagValuesFn(tag, preparedQuery),
                                this.getRecentSearches(),
                            ])];
                    case 1:
                        _b = tslib_1.__read.apply(void 0, [_d.sent(), 2]), tagValues = _b[0], recentSearches = _b[1];
                        return [2 /*return*/, {
                                searchItems: tagValues !== null && tagValues !== void 0 ? tagValues : [],
                                recentSearchItems: recentSearches !== null && recentSearches !== void 0 ? recentSearches : [],
                                tagName: tag.key,
                                type: types_2.ItemType.TAG_VALUE,
                            }];
                }
            });
        }); };
        _this.showDefaultSearches = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var query, _a, defaultSearchItems, defaultRecentItems, tagKeys, recentSearches;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        query = this.state.query;
                        _a = tslib_1.__read(this.props.defaultSearchItems, 2), defaultSearchItems = _a[0], defaultRecentItems = _a[1];
                        if (!!defaultSearchItems.length) return [3 /*break*/, 2];
                        // Update searchTerm, otherwise <SearchDropdown> will have wrong state
                        // (e.g. if you delete a query, the last letter will be highlighted if `searchTerm`
                        // does not get updated)
                        this.setState({ searchTerm: query });
                        tagKeys = this.getTagKeys('');
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 1:
                        recentSearches = _b.sent();
                        this.updateAutoCompleteState(tagKeys, recentSearches !== null && recentSearches !== void 0 ? recentSearches : [], '', types_2.ItemType.TAG_KEY);
                        return [2 /*return*/];
                    case 2:
                        // cursor on whitespace show default "help" search terms
                        this.setState({ searchTerm: '' });
                        this.updateAutoCompleteState(defaultSearchItems, defaultRecentItems, '', types_2.ItemType.DEFAULT);
                        return [2 /*return*/];
                }
            });
        }); };
        _this.updateAutoCompleteFromAst = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var cursor, cursorToken, tagName, node, valueGroup, autocompleteGroups, opGroup_1, node, autocompleteGroups, opGroup_2, opGroup, lastToken, keyText, autocompleteGroups;
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        cursor = this.cursorPosition;
                        cursorToken = this.cursorToken;
                        if (!cursorToken) {
                            this.showDefaultSearches();
                            return [2 /*return*/];
                        }
                        if (!(cursorToken.type === parser_1.Token.Filter)) return [3 /*break*/, 5];
                        tagName = utils_1.getKeyName(cursorToken.key, { aggregateWithArgs: true });
                        if (!utils_1.isWithinToken(cursorToken.value, cursor)) return [3 /*break*/, 2];
                        node = cursorToken.value;
                        return [4 /*yield*/, this.generateValueAutocompleteGroup(tagName, node.text)];
                    case 1:
                        valueGroup = _b.sent();
                        autocompleteGroups = valueGroup ? [valueGroup] : [];
                        // show operator group if at beginning of value
                        if (cursor === node.location.start.offset) {
                            opGroup_1 = generateOpAutocompleteGroup(utils_3.getValidOps(cursorToken), tagName);
                            autocompleteGroups.unshift(opGroup_1);
                        }
                        this.updateAutoCompleteStateMultiHeader(autocompleteGroups);
                        return [2 /*return*/];
                    case 2:
                        if (!utils_1.isWithinToken(cursorToken.key, cursor)) return [3 /*break*/, 4];
                        node = cursorToken.key;
                        return [4 /*yield*/, this.generateTagAutocompleteGroup(tagName)];
                    case 3:
                        autocompleteGroups = [_b.sent()];
                        // show operator group if at end of key
                        if (cursor === node.location.end.offset) {
                            opGroup_2 = generateOpAutocompleteGroup(utils_3.getValidOps(cursorToken), tagName);
                            autocompleteGroups.unshift(opGroup_2);
                        }
                        this.setState({ searchTerm: tagName });
                        this.updateAutoCompleteStateMultiHeader(autocompleteGroups);
                        return [2 /*return*/];
                    case 4:
                        opGroup = generateOpAutocompleteGroup(utils_3.getValidOps(cursorToken), tagName);
                        this.updateAutoCompleteStateMultiHeader([opGroup]);
                        return [2 /*return*/];
                    case 5:
                        if (!(cursorToken.type === parser_1.Token.FreeText)) return [3 /*break*/, 7];
                        lastToken = (_a = cursorToken.text.trim().split(' ').pop()) !== null && _a !== void 0 ? _a : '';
                        keyText = lastToken.replace(new RegExp("^" + constants_1.NEGATION_OPERATOR), '');
                        return [4 /*yield*/, this.generateTagAutocompleteGroup(keyText)];
                    case 6:
                        autocompleteGroups = [_b.sent()];
                        this.setState({ searchTerm: keyText });
                        this.updateAutoCompleteStateMultiHeader(autocompleteGroups);
                        return [2 /*return*/];
                    case 7: return [2 /*return*/];
                }
            });
        }); };
        _this.updateAutoCompleteItems = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var cursor, query, lastTermIndex, terms, last, autoCompleteItems, matchValue, tagName, index, recentSearches, valueGroup;
            var _a, _b, _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        if (this.blurTimeout) {
                            clearTimeout(this.blurTimeout);
                            this.blurTimeout = undefined;
                        }
                        cursor = this.cursorPosition;
                        if (this.hasImprovedSearch) {
                            this.updateAutoCompleteFromAst();
                            return [2 /*return*/];
                        }
                        query = this.state.query;
                        // Don't continue if the query hasn't changed
                        if (query === this.state.previousQuery) {
                            return [2 /*return*/];
                        }
                        this.setState({ previousQuery: query });
                        lastTermIndex = utils_3.getLastTermIndex(query, cursor);
                        terms = utils_3.getQueryTerms(query, lastTermIndex);
                        if (!terms || // no terms
                            terms.length === 0 || // no terms
                            (terms.length === 1 && terms[0] === this.props.defaultQuery) || // default term
                            /^\s+$/.test(query.slice(cursor - 1, cursor + 1))) {
                            this.showDefaultSearches();
                            return [2 /*return*/];
                        }
                        last = (_a = terms.pop()) !== null && _a !== void 0 ? _a : '';
                        index = last.indexOf(':');
                        if (!(index === -1)) return [3 /*break*/, 2];
                        // No colon present; must still be deciding key
                        matchValue = last.replace(new RegExp("^" + constants_1.NEGATION_OPERATOR), '');
                        autoCompleteItems = this.getTagKeys(matchValue);
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 1:
                        recentSearches = _d.sent();
                        this.setState({ searchTerm: matchValue });
                        this.updateAutoCompleteState(autoCompleteItems, recentSearches !== null && recentSearches !== void 0 ? recentSearches : [], matchValue, types_2.ItemType.TAG_KEY);
                        return [2 /*return*/];
                    case 2:
                        // TODO(billy): Better parsing for these examples
                        //
                        // > sentry:release:
                        // > url:"http://with/colon"
                        tagName = last.slice(0, index);
                        // e.g. given "!gpu" we want "gpu"
                        tagName = tagName.replace(new RegExp("^" + constants_1.NEGATION_OPERATOR), '');
                        query = last.slice(index + 1);
                        return [4 /*yield*/, this.generateValueAutocompleteGroup(tagName, query)];
                    case 3:
                        valueGroup = _d.sent();
                        if (valueGroup) {
                            this.updateAutoCompleteState((_b = valueGroup.searchItems) !== null && _b !== void 0 ? _b : [], (_c = valueGroup.recentSearchItems) !== null && _c !== void 0 ? _c : [], valueGroup.tagName, valueGroup.type);
                            return [2 /*return*/];
                        }
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * Updates autocomplete dropdown items and autocomplete index state
         *
         * @param groups Groups that will be used to populate the autocomplete dropdown
         */
        _this.updateAutoCompleteStateMultiHeader = function (groups) {
            var _a = _this.props, hasRecentSearches = _a.hasRecentSearches, maxSearchItems = _a.maxSearchItems, maxQueryLength = _a.maxQueryLength;
            var query = _this.state.query;
            var queryCharsLeft = maxQueryLength && query ? maxQueryLength - query.length : undefined;
            var searchGroups = groups
                .map(function (_a) {
                var searchItems = _a.searchItems, recentSearchItems = _a.recentSearchItems, tagName = _a.tagName, type = _a.type;
                return utils_3.createSearchGroups(searchItems, hasRecentSearches ? recentSearchItems : undefined, tagName, type, maxSearchItems, queryCharsLeft);
            })
                .reduce(function (acc, item) { return ({
                searchGroups: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(acc.searchGroups)), tslib_1.__read(item.searchGroups)),
                flatSearchItems: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(acc.flatSearchItems)), tslib_1.__read(item.flatSearchItems)),
                activeSearchItem: -1,
            }); }, {
                searchGroups: [],
                flatSearchItems: [],
                activeSearchItem: -1,
            });
            _this.setState(searchGroups);
        };
        _this.updateQuery = function (newQuery, cursorPosition) {
            return _this.setState(makeQueryState(newQuery), function () {
                var _a, _b;
                // setting a new input value will lose focus; restore it
                if (_this.searchInput.current) {
                    _this.searchInput.current.focus();
                    if (cursorPosition) {
                        _this.searchInput.current.selectionStart = cursorPosition;
                        _this.searchInput.current.selectionEnd = cursorPosition;
                    }
                }
                // then update the autocomplete box with new items
                _this.updateAutoCompleteItems();
                (_b = (_a = _this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, newQuery, new MouseEvent('click'));
            });
        };
        _this.onAutoCompleteFromAst = function (replaceText, item) {
            var cursor = _this.cursorPosition;
            var query = _this.state.query;
            var cursorToken = _this.cursorToken;
            if (!cursorToken) {
                _this.updateQuery("" + query + replaceText);
                return;
            }
            // the start and end of what to replace
            var clauseStart = null;
            var clauseEnd = null;
            // the new text that will exist between clauseStart and clauseEnd
            var replaceToken = replaceText;
            if (cursorToken.type === parser_1.Token.Filter) {
                if (item.type === types_2.ItemType.TAG_OPERATOR) {
                    analytics_1.trackAnalyticsEvent({
                        eventKey: 'search.operator_autocompleted',
                        eventName: 'Search: Operator Autocompleted',
                        organization_id: _this.props.organization.id,
                        query: utils_3.removeSpace(query),
                        search_operator: replaceText,
                        search_type: _this.props.savedSearchType === 0 ? 'issues' : 'events',
                    });
                    var valueLocation = cursorToken.value.location;
                    clauseStart = cursorToken.location.start.offset;
                    clauseEnd = valueLocation.start.offset;
                    if (replaceText === '!:') {
                        replaceToken = "!" + cursorToken.key.text + ":";
                    }
                    else {
                        replaceToken = "" + cursorToken.key.text + replaceText;
                    }
                }
                else if (utils_1.isWithinToken(cursorToken.value, cursor)) {
                    var location_1 = cursorToken.value.location;
                    var keyLocation = cursorToken.key.location;
                    // Include everything after the ':'
                    clauseStart = keyLocation.end.offset + 1;
                    clauseEnd = location_1.end.offset + 1;
                    replaceToken += ' ';
                }
                else if (utils_1.isWithinToken(cursorToken.key, cursor)) {
                    var location_2 = cursorToken.key.location;
                    clauseStart = location_2.start.offset;
                    // If the token is a key, then trim off the end to avoid duplicate ':'
                    clauseEnd = location_2.end.offset + 1;
                }
            }
            if (cursorToken.type === parser_1.Token.FreeText) {
                clauseStart = cursorToken.location.start.offset;
                clauseEnd = cursorToken.location.end.offset;
            }
            if (clauseStart !== null && clauseEnd !== null) {
                var beforeClause = query.substring(0, clauseStart);
                var endClause = query.substring(clauseEnd);
                var newQuery = "" + beforeClause + replaceToken + endClause;
                _this.updateQuery(newQuery, beforeClause.length + replaceToken.length);
            }
        };
        _this.onAutoComplete = function (replaceText, item) {
            var _a;
            if (item.type === types_2.ItemType.RECENT_SEARCH) {
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'search.searched',
                    eventName: 'Search: Performed search',
                    organization_id: _this.props.organization.id,
                    query: replaceText,
                    source: _this.props.savedSearchType === 0 ? 'issues' : 'events',
                    search_source: 'recent_search',
                });
                _this.setState(makeQueryState(replaceText), function () {
                    // Propagate onSearch and save to recent searches
                    _this.doSearch();
                });
                return;
            }
            var cursor = _this.cursorPosition;
            var query = _this.state.query;
            if (_this.hasImprovedSearch) {
                _this.onAutoCompleteFromAst(replaceText, item);
                return;
            }
            var lastTermIndex = utils_3.getLastTermIndex(query, cursor);
            var terms = utils_3.getQueryTerms(query, lastTermIndex);
            var newQuery;
            // If not postfixed with : (tag value), add trailing space
            replaceText += item.type !== types_2.ItemType.TAG_VALUE || cursor < query.length ? '' : ' ';
            var isNewTerm = query.charAt(query.length - 1) === ' ' && item.type !== types_2.ItemType.TAG_VALUE;
            if (!terms) {
                newQuery = replaceText;
            }
            else if (isNewTerm) {
                newQuery = "" + query + replaceText;
            }
            else {
                var last = (_a = terms.pop()) !== null && _a !== void 0 ? _a : '';
                newQuery = query.slice(0, lastTermIndex); // get text preceding last term
                var prefix = last.startsWith(constants_1.NEGATION_OPERATOR) ? constants_1.NEGATION_OPERATOR : '';
                // newQuery is all the terms up to the current term: "... <term>:"
                // replaceText should be the selected value
                if (last.indexOf(':') > -1) {
                    var replacement = ":" + replaceText;
                    // The user tag often contains : within its value and we need to quote it.
                    if (last.startsWith('user:')) {
                        var colonIndex = replaceText.indexOf(':');
                        if (colonIndex > -1) {
                            replacement = ":\"" + replaceText.trim() + "\"";
                        }
                    }
                    // tag key present: replace everything after colon with replaceText
                    newQuery = newQuery.replace(/\:"[^"]*"?$|\:\S*$/, replacement);
                }
                else {
                    // no tag key present: replace last token with replaceText
                    newQuery = newQuery.replace(/\S+$/, "" + prefix + replaceText);
                }
                newQuery = newQuery.concat(query.slice(lastTermIndex));
            }
            _this.updateQuery(newQuery);
        };
        return _this;
    }
    SmartSearchBar.prototype.componentDidMount = function () {
        if (!window.ResizeObserver) {
            return;
        }
        if (this.containerRef.current === null) {
            return;
        }
        this.inputResizeObserver = new ResizeObserver(this.updateActionsVisible);
        this.inputResizeObserver.observe(this.containerRef.current);
    };
    SmartSearchBar.prototype.componentDidUpdate = function (prevProps) {
        var query = this.props.query;
        var lastQuery = prevProps.query;
        if (query !== lastQuery && (utils_2.defined(query) || utils_2.defined(lastQuery))) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState(makeQueryState(utils_3.addSpace(query !== null && query !== void 0 ? query : undefined)));
        }
    };
    SmartSearchBar.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.inputResizeObserver) === null || _a === void 0 ? void 0 : _a.disconnect();
        if (this.blurTimeout) {
            clearTimeout(this.blurTimeout);
        }
    };
    Object.defineProperty(SmartSearchBar.prototype, "hasImprovedSearch", {
        get: function () {
            return (this.props.organization.features.includes('improved-search') ||
                !!this.props.experimentAssignment);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SmartSearchBar.prototype, "initialQuery", {
        get: function () {
            var _a = this.props, query = _a.query, defaultQuery = _a.defaultQuery;
            return query !== null ? utils_3.addSpace(query) : defaultQuery !== null && defaultQuery !== void 0 ? defaultQuery : '';
        },
        enumerable: false,
        configurable: true
    });
    SmartSearchBar.prototype.blur = function () {
        if (!this.searchInput.current) {
            return;
        }
        this.searchInput.current.blur();
    };
    SmartSearchBar.prototype.doSearch = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var query, _a, onSearch, onSavedRecentSearch, api, organization, savedSearchType, searchSource, err_2;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.blur();
                        if (this.hasImprovedSearch && !this.hasValidSearch) {
                            return [2 /*return*/];
                        }
                        query = utils_3.removeSpace(this.state.query);
                        _a = this.props, onSearch = _a.onSearch, onSavedRecentSearch = _a.onSavedRecentSearch, api = _a.api, organization = _a.organization, savedSearchType = _a.savedSearchType, searchSource = _a.searchSource;
                        analytics_1.trackAnalyticsEvent({
                            eventKey: 'search.searched',
                            eventName: 'Search: Performed search',
                            organization_id: organization.id,
                            query: query,
                            search_type: savedSearchType === 0 ? 'issues' : 'events',
                            search_source: searchSource,
                        });
                        callIfFunction_1.callIfFunction(onSearch, query);
                        // Only save recent search query if we have a savedSearchType (also 0 is a valid value)
                        // Do not save empty string queries (i.e. if they clear search)
                        if (typeof savedSearchType === 'undefined' || !query) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, savedSearches_1.saveRecentSearch(api, organization.slug, savedSearchType, query)];
                    case 2:
                        _b.sent();
                        if (onSavedRecentSearch) {
                            onSavedRecentSearch(query);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _b.sent();
                        // Silently capture errors if it fails to save
                        Sentry.captureException(err_2);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(SmartSearchBar.prototype, "hasValidSearch", {
        /**
         * Check if any filters are invalid within the search query
         */
        get: function () {
            var parsedQuery = this.state.parsedQuery;
            // If we fail to parse be optimistic that it's valid
            if (parsedQuery === null) {
                return true;
            }
            return utils_1.treeResultLocator({
                tree: parsedQuery,
                noResultValue: true,
                visitorTest: function (_a) {
                    var token = _a.token, returnResult = _a.returnResult, skipToken = _a.skipToken;
                    return token.type !== parser_1.Token.Filter
                        ? null
                        : token.invalid
                            ? returnResult(false)
                            : skipToken;
                },
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SmartSearchBar.prototype, "cursorToken", {
        /**
         * Get the active filter or free text actively focused.
         */
        get: function () {
            var parsedQuery = this.state.parsedQuery;
            if (parsedQuery === null) {
                return null;
            }
            var matchedTokens = [parser_1.Token.Filter, parser_1.Token.FreeText];
            var cursor = this.cursorPosition;
            return utils_1.treeResultLocator({
                tree: parsedQuery,
                noResultValue: null,
                visitorTest: function (_a) {
                    var token = _a.token, returnResult = _a.returnResult, skipToken = _a.skipToken;
                    return !matchedTokens.includes(token.type)
                        ? null
                        : utils_1.isWithinToken(token, cursor)
                            ? returnResult(token)
                            : skipToken;
                },
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SmartSearchBar.prototype, "cursorPosition", {
        /**
         * Get the current cursor position within the input
         */
        get: function () {
            var _a;
            if (!this.searchInput.current) {
                return -1;
            }
            // No cursor position when the input loses focus. This is important for
            // updating the search highlighters active state
            if (!this.state.inputHasFocus) {
                return -1;
            }
            return (_a = this.searchInput.current.selectionStart) !== null && _a !== void 0 ? _a : -1;
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Returns array of possible key values that substring match `query`
     */
    SmartSearchBar.prototype.getTagKeys = function (query) {
        var _a;
        var prepareQuery = this.props.prepareQuery;
        var supportedTags = (_a = this.props.supportedTags) !== null && _a !== void 0 ? _a : {};
        // Return all if query is empty
        var tagKeys = Object.keys(supportedTags).map(function (key) { return key + ":"; });
        if (query) {
            var preparedQuery_1 = typeof prepareQuery === 'function' ? prepareQuery(query) : query;
            tagKeys = tagKeys.filter(function (key) { return key.indexOf(preparedQuery_1) > -1; });
        }
        // If the environment feature is active and excludeEnvironment = true
        // then remove the environment key
        if (this.props.excludeEnvironment) {
            tagKeys = tagKeys.filter(function (key) { return key !== 'environment:'; });
        }
        return tagKeys.map(function (value) { return ({ value: value, desc: value }); });
    };
    SmartSearchBar.prototype.generateTagAutocompleteGroup = function (tagName) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var tagKeys, recentSearches;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        tagKeys = this.getTagKeys(tagName);
                        return [4 /*yield*/, this.getRecentSearches()];
                    case 1:
                        recentSearches = _a.sent();
                        return [2 /*return*/, {
                                searchItems: tagKeys,
                                recentSearchItems: recentSearches !== null && recentSearches !== void 0 ? recentSearches : [],
                                tagName: tagName,
                                type: types_2.ItemType.TAG_KEY,
                            }];
                }
            });
        });
    };
    /**
     * Updates autocomplete dropdown items and autocomplete index state
     *
     * @param searchItems List of search item objects with keys: title, desc, value
     * @param recentSearchItems List of recent search items, same format as searchItem
     * @param tagName The current tag name in scope
     * @param type Defines the type/state of the dropdown menu items
     */
    SmartSearchBar.prototype.updateAutoCompleteState = function (searchItems, recentSearchItems, tagName, type) {
        var _a = this.props, hasRecentSearches = _a.hasRecentSearches, maxSearchItems = _a.maxSearchItems, maxQueryLength = _a.maxQueryLength;
        var query = this.state.query;
        var queryCharsLeft = maxQueryLength && query ? maxQueryLength - query.length : undefined;
        this.setState(utils_3.createSearchGroups(searchItems, hasRecentSearches ? recentSearchItems : undefined, tagName, type, maxSearchItems, queryCharsLeft));
    };
    SmartSearchBar.prototype.render = function () {
        var _a = this.props, api = _a.api, className = _a.className, savedSearchType = _a.savedSearchType, dropdownClassName = _a.dropdownClassName, actionBarItems = _a.actionBarItems, organization = _a.organization, placeholder = _a.placeholder, disabled = _a.disabled, useFormWrapper = _a.useFormWrapper, inlineLabel = _a.inlineLabel, maxQueryLength = _a.maxQueryLength;
        var _b = this.state, query = _b.query, parsedQuery = _b.parsedQuery, searchGroups = _b.searchGroups, searchTerm = _b.searchTerm, inputHasFocus = _b.inputHasFocus, numActionsVisible = _b.numActionsVisible, loading = _b.loading;
        var input = (<SearchInput type="text" placeholder={placeholder} id="smart-search-input" name="query" ref={this.searchInput} autoComplete="off" value={query} onFocus={this.onQueryFocus} onBlur={this.onQueryBlur} onKeyUp={this.onKeyUp} onKeyDown={this.onKeyDown} onChange={this.onQueryChange} onClick={this.onInputClick} disabled={disabled} maxLength={maxQueryLength} spellCheck={false}/>);
        // Segment actions into visible and overflowed groups
        var actionItems = actionBarItems !== null && actionBarItems !== void 0 ? actionBarItems : [];
        var actionProps = {
            api: api,
            organization: organization,
            query: query,
            savedSearchType: savedSearchType,
        };
        var visibleActions = actionItems
            .slice(0, numActionsVisible)
            .map(function (_a) {
            var key = _a.key, Action = _a.Action;
            return <Action key={key} {...actionProps}/>;
        });
        var overflowedActions = actionItems
            .slice(numActionsVisible)
            .map(function (_a) {
            var key = _a.key, Action = _a.Action;
            return <Action key={key} {...actionProps} menuItemVariant/>;
        });
        var cursor = this.cursorPosition;
        return (<Container ref={this.containerRef} className={className} isOpen={inputHasFocus}>
        <SearchLabel htmlFor="smart-search-input" aria-label={locale_1.t('Search events')}>
          <icons_1.IconSearch />
          {inlineLabel}
        </SearchLabel>

        <InputWrapper>
          <Highlight>
            {this.hasImprovedSearch && parsedQuery !== null ? (<renderer_1.default parsedQuery={parsedQuery} cursorPosition={cursor === -1 ? undefined : cursor}/>) : (query)}
          </Highlight>
          {useFormWrapper ? <form onSubmit={this.onSubmit}>{input}</form> : input}
        </InputWrapper>

        <ActionsBar gap={0.5}>
          {query !== '' && (<actions_1.ActionButton onClick={this.clearSearch} icon={<icons_1.IconClose size="xs"/>} title={locale_1.t('Clear search')} aria-label={locale_1.t('Clear search')}/>)}
          {visibleActions}
          {overflowedActions.length > 0 && (<dropdownLink_1.default anchorRight caret={false} title={<actions_1.ActionButton aria-label={locale_1.t('Show more')} icon={<VerticalEllipsisIcon size="xs"/>}/>}>
              {overflowedActions}
            </dropdownLink_1.default>)}
        </ActionsBar>

        {(loading || searchGroups.length > 0) && (<searchDropdown_1.default css={{ display: inputHasFocus ? 'block' : 'none' }} className={dropdownClassName} items={searchGroups} onClick={this.onAutoComplete} loading={loading} searchSubstring={searchTerm}/>)}
      </Container>);
    };
    SmartSearchBar.defaultProps = {
        defaultQuery: '',
        query: null,
        onSearch: function () { },
        excludeEnvironment: false,
        placeholder: locale_1.t('Search for events, users, tags, and more'),
        supportedTags: {},
        defaultSearchItems: [[], []],
        useFormWrapper: true,
        savedSearchType: types_1.SavedSearchType.ISSUE,
    };
    return SmartSearchBar;
}(React.Component));
exports.SmartSearchBar = SmartSearchBar;
var SmartSearchBarContainer = /** @class */ (function (_super) {
    tslib_1.__extends(SmartSearchBarContainer, _super);
    function SmartSearchBarContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            members: memberListStore_1.default.getAll(),
        };
        _this.unsubscribe = memberListStore_1.default.listen(function (members) { return _this.setState({ members: members }); }, undefined);
        return _this;
    }
    SmartSearchBarContainer.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    SmartSearchBarContainer.prototype.render = function () {
        // SmartSearchBar doesn't use members, but we forward it to cause a re-render.
        return <SmartSearchBar {...this.props} members={this.state.members}/>;
    };
    return SmartSearchBarContainer;
}(React.Component));
var SmartSearchBarContainerWithExperiment = withExperiment_1.default(SmartSearchBarContainer, {
    experiment: 'ImprovedSearchExperiment',
});
exports.default = withApi_1.default(react_router_1.withRouter(withOrganization_1.default(SmartSearchBarContainerWithExperiment)));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border: 1px solid ", ";\n  box-shadow: inset ", ";\n  background: ", ";\n  padding: 7px ", ";\n  position: relative;\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: start;\n\n  border-radius: ", ";\n\n  .show-sidebar & {\n    background: ", ";\n  }\n"], ["\n  border: 1px solid ", ";\n  box-shadow: inset ", ";\n  background: ", ";\n  padding: 7px ", ";\n  position: relative;\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: start;\n\n  border-radius: ", ";\n\n  .show-sidebar & {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.background; }, space_1.default(1), space_1.default(1), function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " " + p.theme.borderRadius + " 0 0"
        : p.theme.borderRadius;
}, function (p) { return p.theme.backgroundSecondary; });
var SearchLabel = styled_1.default('label')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: ", " 0;\n  margin: 0;\n  color: ", ";\n"], ["\n  display: flex;\n  padding: ", " 0;\n  margin: 0;\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.gray300; });
var InputWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var Highlight = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  user-select: none;\n  white-space: pre-wrap;\n  word-break: break-word;\n  line-height: 25px;\n  font-size: ", ";\n  font-family: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  user-select: none;\n  white-space: pre-wrap;\n  word-break: break-word;\n  line-height: 25px;\n  font-size: ", ";\n  font-family: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.familyMono; });
var SearchInput = styled_1.default(react_autosize_textarea_1.default, {
    shouldForwardProp: function (prop) { return typeof prop === 'string' && is_prop_valid_1.default(prop); },
})(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  resize: none;\n  outline: none;\n  border: 0;\n  width: 100%;\n  padding: 0;\n  line-height: 25px;\n  margin-bottom: -1px;\n  background: transparent;\n  font-size: ", ";\n  font-family: ", ";\n  caret-color: ", ";\n  color: transparent;\n\n  &::selection {\n    background: rgba(0, 0, 0, 0.2);\n  }\n  &::placeholder {\n    color: ", ";\n  }\n\n  [disabled] {\n    color: ", ";\n  }\n"], ["\n  position: relative;\n  display: flex;\n  resize: none;\n  outline: none;\n  border: 0;\n  width: 100%;\n  padding: 0;\n  line-height: 25px;\n  margin-bottom: -1px;\n  background: transparent;\n  font-size: ", ";\n  font-family: ", ";\n  caret-color: ", ";\n  color: transparent;\n\n  &::selection {\n    background: rgba(0, 0, 0, 0.2);\n  }\n  &::placeholder {\n    color: ", ";\n  }\n\n  [disabled] {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.formPlaceholder; }, function (p) { return p.theme.disabled; });
var ActionsBar = styled_1.default(buttonBar_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  height: ", ";\n  margin: ", " 0;\n"], ["\n  height: ", ";\n  margin: ", " 0;\n"])), space_1.default(2), space_1.default(0.5));
var VerticalEllipsisIcon = styled_1.default(icons_1.IconEllipsis)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  transform: rotate(90deg);\n"], ["\n  transform: rotate(90deg);\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map