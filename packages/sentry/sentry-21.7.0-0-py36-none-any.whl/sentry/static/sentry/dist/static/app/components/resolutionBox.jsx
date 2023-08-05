Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var commitLink_1 = tslib_1.__importDefault(require("app/components/commitLink"));
var styles_1 = require("app/components/events/styles");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function renderReason(statusDetails, projectId) {
    var actor = statusDetails.actor ? (<strong>
      <userAvatar_1.default user={statusDetails.actor} size={20} className="avatar"/>
      <span style={{ marginLeft: 5 }}>{statusDetails.actor.name}</span>
    </strong>) : null;
    if (statusDetails.inNextRelease && statusDetails.actor) {
        return locale_1.tct('[actor] marked this issue as resolved in the upcoming release.', {
            actor: actor,
        });
    }
    else if (statusDetails.inNextRelease) {
        return locale_1.t('This issue has been marked as resolved in the upcoming release.');
    }
    else if (statusDetails.inRelease && statusDetails.actor) {
        return locale_1.tct('[actor] marked this issue as resolved in version [version].', {
            actor: actor,
            version: (<version_1.default version={statusDetails.inRelease} projectId={projectId} tooltipRawVersion/>),
        });
    }
    else if (statusDetails.inRelease) {
        return locale_1.tct('This issue has been marked as resolved in version [version].', {
            version: (<version_1.default version={statusDetails.inRelease} projectId={projectId} tooltipRawVersion/>),
        });
    }
    else if (!!statusDetails.inCommit) {
        return locale_1.tct('This issue has been marked as resolved by [commit]', {
            commit: (<react_1.Fragment>
          <commitLink_1.default commitId={statusDetails.inCommit.id} repository={statusDetails.inCommit.repository}/>
          <StyledTimeSince date={statusDetails.inCommit.dateCreated}/>
        </react_1.Fragment>),
        });
    }
    return locale_1.t('This issue has been marked as resolved.');
}
function ResolutionBox(_a) {
    var statusDetails = _a.statusDetails, projectId = _a.projectId;
    return (<styles_1.BannerContainer priority="default">
      <styles_1.BannerSummary>
        <StyledIconCheckmark color="green300"/>
        <span>{renderReason(statusDetails, projectId)}</span>
      </styles_1.BannerSummary>
    </styles_1.BannerContainer>);
}
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(0.5), function (p) { return p.theme.fontSizeSmall; });
var StyledIconCheckmark = styled_1.default(icons_1.IconCheckmark)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  /* override margin defined in BannerSummary */\n  margin-top: 0 !important;\n  align-self: center;\n\n  @media (max-width: ", ") {\n    margin-top: ", " !important;\n    align-self: flex-start;\n  }\n"], ["\n  /* override margin defined in BannerSummary */\n  margin-top: 0 !important;\n  align-self: center;\n\n  @media (max-width: ", ") {\n    margin-top: ", " !important;\n    align-self: flex-start;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(0.5));
exports.default = ResolutionBox;
var templateObject_1, templateObject_2;
//# sourceMappingURL=resolutionBox.jsx.map