Object.defineProperty(exports, "__esModule", { value: true });
exports.experimentConfig = exports.experimentList = exports.unassignedValue = void 0;
var tslib_1 = require("tslib");
var experiments_1 = require("app/types/experiments");
/**
 * This is the value an experiment will have when the unit of assignment
 * (organization, user, etc) is not part of any experiment group.
 *
 * This likely indicates they should see nothing, or the original version of
 * what's being tested.
 */
exports.unassignedValue = -1;
/**
 * Frontend experiment configuration object
 */
exports.experimentList = [
    {
        key: 'DashboardUpsellSandboxExperiment',
        type: experiments_1.ExperimentType.Organization,
        parameter: 'exposed',
        assignments: [0, 1],
    },
    {
        key: 'ImprovedSearchExperiment',
        type: experiments_1.ExperimentType.Organization,
        parameter: 'exposed',
        assignments: [0, 1],
    },
];
exports.experimentConfig = exports.experimentList.reduce(function (acc, exp) {
    var _a;
    return (tslib_1.__assign(tslib_1.__assign({}, acc), (_a = {}, _a[exp.key] = exp, _a)));
}, {});
//# sourceMappingURL=experimentConfig.jsx.map