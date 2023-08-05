Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var avatar_1 = tslib_1.__importDefault(require("app/components/avatar"));
var eventOrGroupHeader_1 = tslib_1.__importDefault(require("app/components/eventOrGroupHeader"));
var linkWithConfirmation_1 = tslib_1.__importDefault(require("app/components/links/linkWithConfirmation"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
function GroupTombstoneRow(_a) {
    var data = _a.data, onUndiscard = _a.onUndiscard;
    var actor = data.actor;
    return (<panels_1.PanelItem center>
      <StyledBox>
        <eventOrGroupHeader_1.default includeLink={false} hideIcons className="truncate" size="normal" data={data}/>
      </StyledBox>
      <AvatarContainer>
        {actor && (<avatar_1.default user={actor} hasTooltip tooltip={locale_1.t('Discarded by %s', actor.name || actor.email)}/>)}
      </AvatarContainer>
      <ActionContainer>
        <tooltip_1.default title={locale_1.t('Undiscard')}>
          <linkWithConfirmation_1.default title={locale_1.t('Undiscard')} className="group-remove btn btn-default btn-sm" message={locale_1.t('Undiscarding this issue means that ' +
            'incoming events that match this will no longer be discarded. ' +
            'New incoming events will count toward your event quota ' +
            'and will display on your issues dashboard. ' +
            'Are you sure you wish to continue?')} onConfirm={function () {
            onUndiscard(data.id);
        }}>
            <icons_1.IconDelete className="undiscard"/>
          </linkWithConfirmation_1.default>
        </tooltip_1.default>
      </ActionContainer>
    </panels_1.PanelItem>);
}
var GroupTombstones = /** @class */ (function (_super) {
    tslib_1.__extends(GroupTombstones, _super);
    function GroupTombstones() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUndiscard = function (tombstoneId) {
            var _a = _this.props, orgId = _a.orgId, projectId = _a.projectId;
            var path = "/projects/" + orgId + "/" + projectId + "/tombstones/" + tombstoneId + "/";
            _this.api
                .requestPromise(path, {
                method: 'DELETE',
            })
                .then(function () {
                indicator_1.addSuccessMessage(locale_1.t('Events similar to these will no longer be filtered'));
                _this.fetchData();
            })
                .catch(function () {
                indicator_1.addErrorMessage(locale_1.t('We were unable to undiscard this issue'));
                _this.fetchData();
            });
        };
        return _this;
    }
    GroupTombstones.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId;
        return [
            ['tombstones', "/projects/" + orgId + "/" + projectId + "/tombstones/", {}, { paginate: true }],
        ];
    };
    GroupTombstones.prototype.renderEmpty = function () {
        return (<panels_1.Panel>
        <emptyMessage_1.default>{locale_1.t('You have no discarded issues')}</emptyMessage_1.default>
      </panels_1.Panel>);
    };
    GroupTombstones.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, tombstones = _a.tombstones, tombstonesPageLinks = _a.tombstonesPageLinks;
        return tombstones.length ? (<react_1.Fragment>
        <panels_1.Panel>
          {tombstones.map(function (data) { return (<GroupTombstoneRow key={data.id} data={data} onUndiscard={_this.handleUndiscard}/>); })}
        </panels_1.Panel>
        {tombstonesPageLinks && <pagination_1.default pageLinks={tombstonesPageLinks}/>}
      </react_1.Fragment>) : (this.renderEmpty());
    };
    return GroupTombstones;
}(asyncComponent_1.default));
var StyledBox = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  align-items: center;\n  min-width: 0; /* keep child content from stretching flex item */\n"], ["\n  flex: 1;\n  align-items: center;\n  min-width: 0; /* keep child content from stretching flex item */\n"])));
var AvatarContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n  width: ", ";\n"], ["\n  margin: 0 ", ";\n  width: ", ";\n"])), space_1.default(4), space_1.default(3));
var ActionContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: ", ";\n"], ["\n  width: ", ";\n"])), space_1.default(4));
exports.default = GroupTombstones;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=groupTombstones.jsx.map