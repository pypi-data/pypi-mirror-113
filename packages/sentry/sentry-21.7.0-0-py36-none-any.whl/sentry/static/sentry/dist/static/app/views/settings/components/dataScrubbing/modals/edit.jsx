Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var modalManager_1 = tslib_1.__importDefault(require("./modalManager"));
var Edit = function (_a) {
    var savedRules = _a.savedRules, rule = _a.rule, props = tslib_1.__rest(_a, ["savedRules", "rule"]);
    var handleGetNewRules = function (values) {
        var updatedRule = tslib_1.__assign(tslib_1.__assign({}, values), { id: rule.id });
        var newRules = savedRules.map(function (savedRule) {
            if (savedRule.id === updatedRule.id) {
                return updatedRule;
            }
            return savedRule;
        });
        return newRules;
    };
    return (<modalManager_1.default {...props} savedRules={savedRules} title={locale_1.t('Edit an advanced data scrubbing rule')} initialState={rule} onGetNewRules={handleGetNewRules}/>);
};
exports.default = Edit;
//# sourceMappingURL=edit.jsx.map