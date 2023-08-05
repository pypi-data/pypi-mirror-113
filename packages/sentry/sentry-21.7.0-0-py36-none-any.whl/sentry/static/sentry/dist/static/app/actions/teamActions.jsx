Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var TeamActions = reflux_1.default.createActions([
    'createTeam',
    'createTeamError',
    'createTeamSuccess',
    'fetchAll',
    'fetchAllError',
    'fetchAllSuccess',
    'fetchDetails',
    'fetchDetailsError',
    'fetchDetailsSuccess',
    'loadTeams',
    'removeTeam',
    'removeTeamError',
    'removeTeamSuccess',
    'update',
    'updateError',
    'updateSuccess',
]);
exports.default = TeamActions;
//# sourceMappingURL=teamActions.jsx.map