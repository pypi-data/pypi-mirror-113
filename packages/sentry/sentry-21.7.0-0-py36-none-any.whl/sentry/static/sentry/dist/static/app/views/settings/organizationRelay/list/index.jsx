Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var orderBy_1 = tslib_1.__importDefault(require("lodash/orderBy"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var activityList_1 = tslib_1.__importDefault(require("./activityList"));
var cardHeader_1 = tslib_1.__importDefault(require("./cardHeader"));
var utils_1 = require("./utils");
var waitingActivity_1 = tslib_1.__importDefault(require("./waitingActivity"));
var List = function (_a) {
    var relays = _a.relays, relayActivities = _a.relayActivities, onRefresh = _a.onRefresh, onDelete = _a.onDelete, onEdit = _a.onEdit, disabled = _a.disabled;
    var orderedRelays = orderBy_1.default(relays, function (relay) { return relay.created; }, ['desc']);
    var relaysByPublicKey = utils_1.getRelaysByPublicKey(orderedRelays, relayActivities);
    var renderCardContent = function (activities) {
        if (!activities.length) {
            return <waitingActivity_1.default onRefresh={onRefresh} disabled={disabled}/>;
        }
        return <activityList_1.default activities={activities}/>;
    };
    return (<Wrapper>
      {Object.keys(relaysByPublicKey).map(function (relayByPublicKey) {
            var _a = relaysByPublicKey[relayByPublicKey], name = _a.name, description = _a.description, created = _a.created, activities = _a.activities;
            return (<Card key={relayByPublicKey}>
            <cardHeader_1.default publicKey={relayByPublicKey} name={name} description={description} created={created} onEdit={onEdit} onDelete={onDelete} disabled={disabled}/>
            {renderCardContent(activities)}
          </Card>);
        })}
    </Wrapper>);
};
exports.default = List;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(3));
var Card = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map