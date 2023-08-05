Object.defineProperty(exports, "__esModule", { value: true });
exports.findMatchedRules = void 0;
var tslib_1 = require("tslib");
/**
 * Given a list of rule objects returned from the API, locate the matching
 * rules for a specific owner.
 */
function findMatchedRules(rules, owner) {
    if (!rules) {
        return undefined;
    }
    var matchOwner = function (actorType, key) {
        return (actorType === 'user' && key === owner.email) ||
            (actorType === 'team' && key === owner.name);
    };
    var actorHasOwner = function (_a) {
        var _b = tslib_1.__read(_a, 2), actorType = _b[0], key = _b[1];
        return actorType === owner.type && matchOwner(actorType, key);
    };
    return rules
        .filter(function (_a) {
        var _b = tslib_1.__read(_a, 2), _ = _b[0], ruleActors = _b[1];
        return ruleActors.find(actorHasOwner);
    })
        .map(function (_a) {
        var _b = tslib_1.__read(_a, 1), rule = _b[0];
        return rule;
    });
}
exports.findMatchedRules = findMatchedRules;
//# sourceMappingURL=findMatchedRules.jsx.map