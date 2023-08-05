Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var teamAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/teamAvatar"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var ActorAvatar = /** @class */ (function (_super) {
    tslib_1.__extends(ActorAvatar, _super);
    function ActorAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ActorAvatar.prototype.render = function () {
        var _a;
        var _b = this.props, actor = _b.actor, props = tslib_1.__rest(_b, ["actor"]);
        if (actor.type === 'user') {
            var user = actor.id ? (_a = memberListStore_1.default.getById(actor.id)) !== null && _a !== void 0 ? _a : actor : actor;
            return <userAvatar_1.default user={user} {...props}/>;
        }
        if (actor.type === 'team') {
            var team = teamStore_1.default.getById(actor.id);
            return <teamAvatar_1.default team={team} {...props}/>;
        }
        Sentry.withScope(function (scope) {
            scope.setExtra('actor', actor);
            Sentry.captureException(new Error('Unknown avatar type'));
        });
        return null;
    };
    ActorAvatar.defaultProps = {
        size: 24,
        hasTooltip: true,
    };
    return ActorAvatar;
}(React.Component));
exports.default = ActorAvatar;
//# sourceMappingURL=actorAvatar.jsx.map