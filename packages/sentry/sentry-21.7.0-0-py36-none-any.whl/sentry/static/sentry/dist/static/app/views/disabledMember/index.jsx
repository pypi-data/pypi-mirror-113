Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var notFound_1 = tslib_1.__importDefault(require("app/components/errors/notFound"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
// getsentry will add the view
var DisabledMemberComponent = hookOrDefault_1.default({
    hookName: 'component:disabled-member',
    defaultComponent: function () { return <notFound_1.default />; },
});
exports.default = DisabledMemberComponent;
//# sourceMappingURL=index.jsx.map