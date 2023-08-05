Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var modalManager_1 = tslib_1.__importDefault(require("./modalManager"));
var Add = function (_a) {
    var savedRules = _a.savedRules, props = tslib_1.__rest(_a, ["savedRules"]);
    var handleGetNewRules = function (values) {
        return tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(savedRules)), [tslib_1.__assign(tslib_1.__assign({}, values), { id: savedRules.length })]);
    };
    return (<modalManager_1.default {...props} savedRules={savedRules} title={locale_1.t('Add an advanced data scrubbing rule')} onGetNewRules={handleGetNewRules}/>);
};
exports.default = Add;
//# sourceMappingURL=add.jsx.map