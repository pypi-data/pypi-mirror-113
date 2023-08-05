Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var framer_motion_1 = require("framer-motion");
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var locale_1 = require("app/locale");
var setupIntroduction_1 = tslib_1.__importDefault(require("./setupIntroduction"));
function FullIntroduction(_a) {
    var _b, _c;
    var currentPlatform = _a.currentPlatform;
    return (<React.Fragment>
      <setupIntroduction_1.default stepHeaderText={locale_1.t('Prepare the %s SDK', (_c = (_b = platforms_1.default.find(function (p) { return p.id === currentPlatform; })) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '')} platform={currentPlatform}/>
      <framer_motion_1.motion.p variants={{
            initial: { opacity: 0 },
            animate: { opacity: 1 },
            exit: { opacity: 0 },
        }}>
        {locale_1.tct("Don't have a relationship with your terminal? [link:Invite your team instead].", {
            link: (<button_1.default priority="link" data-test-id="onboarding-getting-started-invite-members" onClick={modal_1.openInviteMembersModal}/>),
        })}
      </framer_motion_1.motion.p>
    </React.Fragment>);
}
exports.default = FullIntroduction;
//# sourceMappingURL=fullIntroduction.jsx.map