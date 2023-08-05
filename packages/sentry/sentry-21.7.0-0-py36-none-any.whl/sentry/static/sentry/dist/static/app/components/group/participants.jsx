Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var sidebarSection_1 = tslib_1.__importDefault(require("./sidebarSection"));
var GroupParticipants = function (_a) {
    var participants = _a.participants;
    return (<sidebarSection_1.default title={locale_1.tn('%s Participant', '%s Participants', participants.length)}>
    <Faces>
      {participants.map(function (user) { return (<Face key={user.username}>
          <userAvatar_1.default size={28} user={user} hasTooltip/>
        </Face>); })}
    </Faces>
  </sidebarSection_1.default>);
};
exports.default = GroupParticipants;
var Faces = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var Face = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-right: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(0.5), space_1.default(0.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=participants.jsx.map