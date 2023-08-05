Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
// TODO(dcramer): we should probably just make every parameter update
// work on bulk groups
var GroupActions = reflux_1.default.createActions([
    'assignTo',
    'assignToError',
    'assignToSuccess',
    'delete',
    'deleteError',
    'deleteSuccess',
    'discard',
    'discardError',
    'discardSuccess',
    'update',
    'updateError',
    'updateSuccess',
    'merge',
    'mergeError',
    'mergeSuccess',
    'populateStats',
]);
exports.default = GroupActions;
//# sourceMappingURL=groupActions.jsx.map