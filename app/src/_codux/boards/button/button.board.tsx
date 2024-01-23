import { createBoard } from '@wixc3/react-board';
import { Button } from '../../../components/ui/button';

export default createBoard({
    name: 'Button',
    Board: () => <Button />,
    isSnippet: true,
});
