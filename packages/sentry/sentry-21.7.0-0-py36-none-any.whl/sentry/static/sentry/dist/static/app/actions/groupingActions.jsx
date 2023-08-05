Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
// Actions for "Grouping" view - for merging/unmerging events/issues
var GroupingActions = reflux_1.default.createActions([
    'fetch',
    'showAllSimilarItems',
    'toggleUnmerge',
    'toggleMerge',
    'unmerge',
    'merge',
    'toggleCollapseFingerprint',
    'toggleCollapseFingerprints',
]);
exports.default = GroupingActions;
//# sourceMappingURL=groupingActions.jsx.map