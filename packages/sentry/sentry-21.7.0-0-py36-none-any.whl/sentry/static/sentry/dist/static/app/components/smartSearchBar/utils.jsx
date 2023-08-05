Object.defineProperty(exports, "__esModule", { value: true });
exports.getValidOps = exports.generateOperatorEntryMap = exports.filterSearchGroupsByIndex = exports.createSearchGroups = exports.getQueryTerms = exports.getLastTermIndex = exports.removeSpace = exports.addSpace = void 0;
var tslib_1 = require("tslib");
var parser_1 = require("app/components/searchSyntax/parser");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var types_1 = require("./types");
function addSpace(query) {
    if (query === void 0) { query = ''; }
    if (query.length !== 0 && query[query.length - 1] !== ' ') {
        return query + ' ';
    }
    return query;
}
exports.addSpace = addSpace;
function removeSpace(query) {
    if (query === void 0) { query = ''; }
    if (query[query.length - 1] === ' ') {
        return query.slice(0, query.length - 1);
    }
    return query;
}
exports.removeSpace = removeSpace;
/**
 * Given a query, and the current cursor position, return the string-delimiting
 * index of the search term designated by the cursor.
 */
function getLastTermIndex(query, cursor) {
    // TODO: work with quoted-terms
    var cursorOffset = query.slice(cursor).search(/\s|$/);
    return cursor + (cursorOffset === -1 ? 0 : cursorOffset);
}
exports.getLastTermIndex = getLastTermIndex;
/**
 * Returns an array of query terms, including incomplete terms
 *
 * e.g. ["is:unassigned", "browser:\"Chrome 33.0\"", "assigned"]
 */
function getQueryTerms(query, cursor) {
    return query.slice(0, cursor).match(/\S+:"[^"]*"?|\S+/g);
}
exports.getQueryTerms = getQueryTerms;
function getTitleForType(type) {
    if (type === types_1.ItemType.TAG_VALUE) {
        return locale_1.t('Tag Values');
    }
    if (type === types_1.ItemType.RECENT_SEARCH) {
        return locale_1.t('Recent Searches');
    }
    if (type === types_1.ItemType.DEFAULT) {
        return locale_1.t('Common Search Terms');
    }
    if (type === types_1.ItemType.TAG_OPERATOR) {
        return locale_1.t('Operator Helpers');
    }
    return locale_1.t('Tags');
}
function getIconForTypeAndTag(type, tagName) {
    if (type === types_1.ItemType.RECENT_SEARCH) {
        return <icons_1.IconClock size="xs"/>;
    }
    if (type === types_1.ItemType.DEFAULT) {
        return <icons_1.IconStar size="xs"/>;
    }
    // Change based on tagName and default to "icon-tag"
    switch (tagName) {
        case 'is':
            return <icons_1.IconToggle size="xs"/>;
        case 'assigned':
        case 'bookmarks':
            return <icons_1.IconUser size="xs"/>;
        case 'firstSeen':
        case 'lastSeen':
        case 'event.timestamp':
            return <icons_1.IconClock size="xs"/>;
        default:
            return <icons_1.IconTag size="xs"/>;
    }
}
function createSearchGroups(searchItems, recentSearchItems, tagName, type, maxSearchItems, queryCharsLeft) {
    var activeSearchItem = 0;
    if (maxSearchItems && maxSearchItems > 0) {
        searchItems = searchItems.filter(function (value, index) {
            return index < maxSearchItems || value.ignoreMaxSearchItems;
        });
    }
    if (queryCharsLeft || queryCharsLeft === 0) {
        searchItems = searchItems.filter(function (value) { return value.value.length <= queryCharsLeft; });
        if (recentSearchItems) {
            recentSearchItems = recentSearchItems.filter(function (value) { return value.value.length <= queryCharsLeft; });
        }
    }
    var searchGroup = {
        title: getTitleForType(type),
        type: type === types_1.ItemType.INVALID_TAG ? type : 'header',
        icon: getIconForTypeAndTag(type, tagName),
        children: tslib_1.__spreadArray([], tslib_1.__read(searchItems)),
    };
    var recentSearchGroup = recentSearchItems && {
        title: locale_1.t('Recent Searches'),
        type: 'header',
        icon: <icons_1.IconClock size="xs"/>,
        children: tslib_1.__spreadArray([], tslib_1.__read(recentSearchItems)),
    };
    if (searchGroup.children && !!searchGroup.children.length) {
        searchGroup.children[activeSearchItem] = tslib_1.__assign({}, searchGroup.children[activeSearchItem]);
    }
    return {
        searchGroups: tslib_1.__spreadArray([searchGroup], tslib_1.__read((recentSearchGroup ? [recentSearchGroup] : []))),
        flatSearchItems: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(searchItems)), tslib_1.__read((recentSearchItems ? recentSearchItems : []))),
        activeSearchItem: -1,
    };
}
exports.createSearchGroups = createSearchGroups;
/**
 * Items is a list of dropdown groups that have a `children` field. Only the
 * `children` are selectable, so we need to find which child is selected given
 * an index that is in range of the sum of all `children` lengths
 *
 * @return Returns a tuple of [groupIndex, childrenIndex]
 */
function filterSearchGroupsByIndex(items, index) {
    var _index = index;
    var foundSearchItem = [undefined, undefined];
    items.find(function (_a, i) {
        var children = _a.children;
        if (!children || !children.length) {
            return false;
        }
        if (_index < children.length) {
            foundSearchItem = [i, _index];
            return true;
        }
        _index -= children.length;
        return false;
    });
    return foundSearchItem;
}
exports.filterSearchGroupsByIndex = filterSearchGroupsByIndex;
function generateOperatorEntryMap(tag) {
    var _a;
    return _a = {},
        _a[parser_1.TermOperator.Default] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':',
            desc: tag + ":" + locale_1.t('[value] is equal to'),
        },
        _a[parser_1.TermOperator.GreaterThanEqual] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':>=',
            desc: tag + ":" + locale_1.t('>=[value] is greater than or equal to'),
        },
        _a[parser_1.TermOperator.LessThanEqual] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':<=',
            desc: tag + ":" + locale_1.t('<=[value] is less than or equal to'),
        },
        _a[parser_1.TermOperator.GreaterThan] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':>',
            desc: tag + ":" + locale_1.t('>[value] is greater than'),
        },
        _a[parser_1.TermOperator.LessThan] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':<',
            desc: tag + ":" + locale_1.t('<[value] is less than'),
        },
        _a[parser_1.TermOperator.Equal] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: ':=',
            desc: tag + ":" + locale_1.t('=[value] is equal to'),
        },
        _a[parser_1.TermOperator.NotEqual] = {
            type: types_1.ItemType.TAG_OPERATOR,
            value: '!:',
            desc: "!" + tag + ":" + locale_1.t('[value] is not equal to'),
        },
        _a;
}
exports.generateOperatorEntryMap = generateOperatorEntryMap;
function getValidOps(filterToken) {
    var _a, _b;
    // If the token is invalid we want to use the possible expected types as our filter type
    var validTypes = (_b = (_a = filterToken.invalid) === null || _a === void 0 ? void 0 : _a.expectedType) !== null && _b !== void 0 ? _b : [filterToken.filter];
    // Determine any interchangable filter types for our valid types
    var interchangeableTypes = validTypes.map(function (type) { var _a; return (_a = parser_1.interchangeableFilterOperators[type]) !== null && _a !== void 0 ? _a : []; });
    // Combine all types
    var allValidTypes = tslib_1.__spreadArray([], tslib_1.__read(new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(validTypes)), tslib_1.__read(interchangeableTypes.flat())))));
    // Find all valid operations
    var validOps = new Set(allValidTypes.map(function (type) { return parser_1.filterTypeConfig[type].validOps; }).flat());
    return tslib_1.__spreadArray([], tslib_1.__read(validOps));
}
exports.getValidOps = getValidOps;
//# sourceMappingURL=utils.jsx.map