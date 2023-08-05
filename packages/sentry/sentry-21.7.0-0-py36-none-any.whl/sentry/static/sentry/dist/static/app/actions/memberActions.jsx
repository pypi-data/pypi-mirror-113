Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var MemberActions = reflux_1.default.createActions([
    'createSuccess',
    'update',
    'updateError',
    'updateSuccess',
    'resendMemberInvite',
    'resendMemberInviteSuccess',
    'resendMemberInviteError',
]);
exports.default = MemberActions;
//# sourceMappingURL=memberActions.jsx.map