Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var flatMap_1 = tslib_1.__importDefault(require("lodash/flatMap"));
function hasRootGroup(items) {
    var _a;
    return !!((_a = items[0]) === null || _a === void 0 ? void 0 : _a.items);
}
function filterItems(items, inputValue) {
    return items.filter(function (item) {
        return (item.searchKey || item.value + " " + item.label)
            .toLowerCase()
            .indexOf(inputValue.toLowerCase()) > -1;
    });
}
function filterGroupedItems(groups, inputValue) {
    return groups
        .map(function (group) { return (tslib_1.__assign(tslib_1.__assign({}, group), { items: filterItems(group.items, inputValue) })); })
        .filter(function (group) { return group.items.length > 0; });
}
function autoCompleteFilter(items, inputValue) {
    var itemCount = 0;
    if (!items) {
        return [];
    }
    if (hasRootGroup(items)) {
        // if the first item has children, we assume it is a group
        return flatMap_1.default(filterGroupedItems(items, inputValue), function (item) {
            var groupItems = item.items.map(function (groupedItem) { return (tslib_1.__assign(tslib_1.__assign({}, groupedItem), { index: itemCount++ })); });
            // Make sure we don't add the group label to list of items
            // if we try to hide it, otherwise it will render if the list
            // is using virtualized rows (because of fixed row heights)
            if (item.hideGroupLabel) {
                return groupItems;
            }
            return tslib_1.__spreadArray([tslib_1.__assign(tslib_1.__assign({}, item), { groupLabel: true })], tslib_1.__read(groupItems));
        });
    }
    return filterItems(items, inputValue).map(function (item, index) { return (tslib_1.__assign(tslib_1.__assign({}, item), { index: index })); });
}
exports.default = autoCompleteFilter;
//# sourceMappingURL=autoCompleteFilter.jsx.map