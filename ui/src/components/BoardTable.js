
import { mockHighLevelAcessData } from '../utils/utils';

export default function BoardTable() {
    const data = mockHighLevelAcessData(15, 10);
    console.log(data);
    
    return (
      <div className=''>
        Testing Table goes here
      </div>
    );

  }