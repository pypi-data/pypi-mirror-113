Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var GuideActions = reflux_1.default.createActions([
    'closeGuide',
    'fetchSucceeded',
    'nextStep',
    'toStep',
    'registerAnchor',
    'unregisterAnchor',
]);
exports.default = GuideActions;
//# sourceMappingURL=guideActions.jsx.map